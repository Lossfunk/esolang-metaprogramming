#!/usr/bin/env bash
# Drive a pi benchmark cell headlessly, using the operator's FULL personal pi
# config (global ~/.pi/agent/AGENTS.md, extensions, skills) as the agent
# wrapper -- that personal config is exactly what's under test here.
#
# Usage:
#   pi/run_cell.sh --model <id> --language <lang> [--max-turns N] [--max-problems N] [--dataset-file PATH]
#
# --model is REQUIRED. There is no default -- an omitted --model is an error,
# by design (the operator picks the model deliberately per run).
#
# Requires (in order):
#   1. pi/load_dataset.py has been run (real dataset present, see --dataset-file).
#   2. pi/setup_cells.py has been run (cell dir with harness.py + AGENTS.md symlinks exists).
#
# SAFETY (learned the hard way): the child `pi` is a SEPARATE process/session
# from whatever pi session launched this script. If this repo is a `bench`-
# managed clone, the bench-lock guard will BLOCK the child's bash/read/write
# entirely unless it's given an authorized session id -- pass one via
# --session-id (mint it with the `bench` tool's grant:true option in the
# LAUNCHING session first). Separately, by default the child's tool surface is
# restricted to read/bash/edit/write only (--tools), NOT the full extension
# set -- an earlier run let the child discover and call craft_takeover on the
# launching session's OWN live craft workflow, rebinding it out from under
# that session. Override with --allowed-tools if you understand that risk.
set -euo pipefail

PI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PI_DIR/.." && pwd)"

MODEL=""
LANGUAGE=""
MAX_TURNS=40
MAX_PROBLEMS=""
DATASET_FILE="$REPO_ROOT/benchmark_harness/private/esolang_full_private.local.json"
SESSION_ID_OVERRIDE=""
ALLOWED_TOOLS="read,bash,edit,write"

usage() {
  cat >&2 <<EOF
Usage: $0 --model <id> --language <brainfuck|befunge-98|whitespace|shakespeare> [options]

Required:
  --model <id>            Model id/pattern to pass to pi (e.g. anthropic/claude-sonnet-4-6).
                           REQUIRED -- there is no default, this errors out if omitted.
  --language <lang>       One of: brainfuck, befunge-98, whitespace, shakespeare

Options:
  --max-turns N           Max pi invocations before bailing (default: $MAX_TURNS)
  --max-problems N        Stop once N problems have been finalized (solved/failed/skipped)
                           -- for smoke-testing; default: unset = run to all 80
  --dataset-file PATH     Private JSON to use as HARNESS_PRIVATE_FILE
                           (default: benchmark_harness/private/esolang_full_private.local.json)
  --session-id ID         pi session id for the child (default: pi-esolang-<language>).
                           If this repo is a bench-managed clone, pass a grant token here
                           (see the SAFETY note above) or the child's bash/read/write will
                           be blocked by the bench-lock guard.
  --allowed-tools LIST    Comma-separated pi --tools allowlist for the child
                           (default: $ALLOWED_TOOLS -- deliberately excludes
                           craft_*/initiative_*/bench/ask_user_question/mcp).
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="${2:-}"; shift 2 ;;
    --language) LANGUAGE="${2:-}"; shift 2 ;;
    --max-turns) MAX_TURNS="${2:-}"; shift 2 ;;
    --max-problems) MAX_PROBLEMS="${2:-}"; shift 2 ;;
    --dataset-file) DATASET_FILE="${2:-}"; shift 2 ;;
    --session-id) SESSION_ID_OVERRIDE="${2:-}"; shift 2 ;;
    --allowed-tools) ALLOWED_TOOLS="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "ERROR: unknown argument: $1" >&2; usage ;;
  esac
done

if [[ -z "$MODEL" ]]; then
  echo "ERROR: --model is required (no default is provided by design)." >&2
  exit 1
fi
if [[ -z "$LANGUAGE" ]]; then
  echo "ERROR: --language is required." >&2
  exit 1
fi

CELL_DIR="$REPO_ROOT/experiments/01_main_experiments/pi/$LANGUAGE"
if [[ ! -d "$CELL_DIR" ]]; then
  echo "ERROR: cell not found at $CELL_DIR -- run: python3 pi/setup_cells.py" >&2
  exit 1
fi
if [[ ! -f "$DATASET_FILE" ]]; then
  echo "ERROR: dataset file not found at $DATASET_FILE -- run: python3 pi/load_dataset.py" >&2
  exit 1
fi

cd "$CELL_DIR"
export HARNESS_PRIVATE_FILE="$DATASET_FILE"

if [[ ! -f harness_state.json ]]; then
  echo "[run_cell] initializing harness session for $LANGUAGE"
  python3 harness.py init --language "$LANGUAGE"
fi

SESSION_DIR="$CELL_DIR/.pi-sessions"
mkdir -p "$SESSION_DIR"
SESSION_ID="${SESSION_ID_OVERRIDE:-pi-esolang-$LANGUAGE}"

status_field() {
  # $1: field label as printed by harness.py status, e.g. "Solved:"
  python3 harness.py status | awk -v f="$1" '$0 ~ "^"f {print $2}'
}

for ((i = 1; i <= MAX_TURNS; i++)); do
  solved=$(status_field "Solved:")
  failed=$(status_field "Failed:")
  skipped=$(status_field "Skipped:")
  active=$(status_field "Active:")
  remaining=$(status_field "Remaining:")
  finalized=$((solved + failed + skipped))

  echo "[run_cell] turn $i/$MAX_TURNS -- solved=$solved failed=$failed skipped=$skipped active=$active remaining=$remaining"

  if [[ -n "$MAX_PROBLEMS" && "$finalized" -ge "$MAX_PROBLEMS" ]]; then
    echo "[run_cell] reached --max-problems=$MAX_PROBLEMS finalized problems, stopping."
    break
  fi
  if [[ "$remaining" -eq 0 && "$active" -eq 0 ]]; then
    echo "[run_cell] all 80 problems finalized, stopping."
    break
  fi

  if [[ "$i" -eq 1 ]]; then
    PROMPT='Read AGENTS.md and follow it exactly. This session is initialized. Begin with: python3 harness.py fetch. Solve problems in order. Use python3 harness.py run <file> --input "..." to test. Then python3 harness.py submit <id> <file>. Max 3 submissions per problem.'
  else
    PROMPT='Continue. Run python3 harness.py status if unsure where you left off, then proceed with the current or next problem exactly per AGENTS.md.'
  fi

  # A per-turn timeout is EXPECTED (a small model can take minutes to work
  # through fetch->write->run->submit in one autonomous turn) -- tolerate it
  # and let the next loop iteration pick up wherever harness_state.json
  # actually landed, rather than aborting the whole driver on `set -e`.
  set +e
  timeout "${PI_TURN_TIMEOUT:-300}" pi -p --model "$MODEL" --session-dir "$SESSION_DIR" \
    --session-id "$SESSION_ID" --tools "$ALLOWED_TOOLS" -a "$PROMPT"
  turn_rc=$?
  set -e
  if [[ "$turn_rc" -eq 124 ]]; then
    echo "[run_cell] turn $i timed out after ${PI_TURN_TIMEOUT:-300}s -- continuing to next turn"
  elif [[ "$turn_rc" -ne 0 ]]; then
    echo "[run_cell] turn $i exited $turn_rc -- continuing to next turn"
  fi
done

python3 harness.py export
echo "[run_cell] done. export.json written in $CELL_DIR"
