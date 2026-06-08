#!/usr/bin/env bash
# End-to-end smoke test that the harness is wired correctly without
# making any provider API calls.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUPP_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

TMP_CELL="$(mktemp -d)"
trap 'rm -rf "$TMP_CELL"' EXIT

echo "[1] Symlinking shared harness into a temporary cell at $TMP_CELL"
ln -s "$SUPP_ROOT/benchmark_harness/harness.py" "$TMP_CELL/harness.py"
ln -s "$SUPP_ROOT/prompts/brainfuck/CLAUDE.md" "$TMP_CELL/CLAUDE.md"

cd "$TMP_CELL"

echo "[2] init --language brainfuck"
python harness.py init --language brainfuck >/dev/null
test -f harness_state.json
echo "    OK ($(wc -c <harness_state.json) bytes of state)"

echo "[3] fetch (should reveal E01)"
python harness.py fetch | head -3

echo "[4] run a tiny BF program (echoes input chars)"
echo ',[.,]' > echo.bf
out=$(python harness.py run echo.bf --input "hi" 2>&1 || true)
echo "    output: $out"

echo "[5] status"
python harness.py status | head -5

echo
echo "OK - harness smoke test passed (no provider API calls were made)."
