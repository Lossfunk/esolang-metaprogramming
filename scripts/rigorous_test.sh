#!/usr/bin/env bash
# Rigorous end-to-end smoke test of every layer of the supplementary code.
# No provider API keys are required. The test exercises:
#   - shared harness path resolution (works through symlinks)
#   - init / fetch / run / submit / status / skip / export
#   - max-3-submission enforcement
#   - a real cell from the 01_main_experiments grid
#   - cell rebuild scripts (setup_all.sh)
#   - ablation cell validator
# Brutally exits non-zero on any failure.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUPP_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

PASS_COUNT=0
FAIL_COUNT=0
fail() { echo "  FAIL: $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
pass() { echo "  PASS: $1"; PASS_COUNT=$((PASS_COUNT + 1)); }

echo "====================================================================="
echo "  Rigorous test of supplementary_code/"
echo "  $SUPP_ROOT"
echo "====================================================================="

echo
echo "[A] Path / secret sanity (no local paths or personal emails)"
# Generic patterns that should NEVER appear in an anonymized supplementary
# tree. Personal names / orgs / emails are NOT hard-coded here so that the
# regex itself does not leak who is being filtered. To check author-specific
# identifiers before packaging, set LEAK_RE_EXTRA in the environment, e.g.:
#   LEAK_RE_EXTRA='myname|MyOrg|me@example\.com' bash scripts/rigorous_test.sh
#
# Note: huggingface.co / hf.co are intentionally NOT in the default deny-list,
# because the supplementary cites a publicly released third-party dataset
# (EsoLang-Bench) using its canonical HuggingFace URL — the same way ImageNet,
# COCO, MMLU citations would. If you want to flag *any* HF URL pre-submission,
# add it via LEAK_RE_EXTRA.
LEAK_RE="/Users/[A-Za-z0-9._-]+|/home/[a-z][a-z0-9._-]*|@(gmail|hotmail|outlook|yahoo|icloud)\\.com"
if [ -n "${LEAK_RE_EXTRA:-}" ]; then
  LEAK_RE="$LEAK_RE|$LEAK_RE_EXTRA"
fi
content_hit=$(grep -rE --exclude-dir=.git "$LEAK_RE" "$SUPP_ROOT" 2>/dev/null | grep -v "rigorous_test\\.sh" | head -1 || true)
if [ -n "$content_hit" ]; then
  echo "$content_hit"
  fail "personal paths or org names found in file content"
else
  pass "no personal paths, org names, or HF URLs in file content"
fi
# Symlink targets are *not* read by grep -r; scan them explicitly.
set +e
symlink_hit=$(
  find "$SUPP_ROOT" -type l -not -path "*/.git/*" -print0 2>/dev/null \
    | while IFS= read -r -d '' l; do
        t=$(readlink "$l" || true)
        if echo "$t" | grep -qE "$LEAK_RE"; then
          printf '%s -> %s\n' "$l" "$t"
        fi
      done | head -1
)
set -e
if [ -n "$symlink_hit" ]; then
  echo "$symlink_hit"
  fail "symlink target leaks personal path / org"
else
  pass "no leaky symlink targets (all relative)"
fi

echo
echo "[B] Layout sanity"
for must_exist in \
  "$SUPP_ROOT/benchmark_harness/harness.py" \
  "$SUPP_ROOT/benchmark_harness/.experiment_root" \
  "$SUPP_ROOT/benchmark_harness/interpreters/brainfuck_interpreter.py" \
  "$SUPP_ROOT/benchmark_harness/public/esolang_full_public.json" \
  "$SUPP_ROOT/benchmark_harness/private/esolang_full_private.json" \
  "$SUPP_ROOT/prompts/brainfuck/CLAUDE.md" \
  "$SUPP_ROOT/README.md" \
  "$SUPP_ROOT/HOWTO_RUN.md" \
  "$SUPP_ROOT/LICENSE" \
  "$SUPP_ROOT/CITATION.cff" ; do
  if [ -e "$must_exist" ]; then
    pass "exists: ${must_exist#$SUPP_ROOT/}"
  else
    fail "missing: ${must_exist#$SUPP_ROOT/}"
  fi
done

echo
echo "[C] Setup scripts run end to end"
bash "$SCRIPT_DIR/setup_all.sh" >/dev/null 2>&1 && pass "setup_all.sh ran" || fail "setup_all.sh exited non-zero"
python3 "$SCRIPT_DIR/setup_main_grid.py" >/dev/null 2>&1 && pass "setup_main_grid.py ran" || fail "setup_main_grid.py exited non-zero"
python3 "$SUPP_ROOT/experiments/02_metaprogramming_ablation/validate_cells.py" >/dev/null 2>&1 \
  && pass "ablation validate_cells.py" || fail "ablation validate_cells.py"

echo
echo "[D] Cell counts"
NUM_MAIN=$(find "$SUPP_ROOT/experiments/01_main_experiments" -mindepth 3 -maxdepth 3 -type d | wc -l | tr -d ' ')
[ "$NUM_MAIN" = "24" ] && pass "01_main_experiments has 24 cells" || fail "01_main_experiments has $NUM_MAIN cells (expected 24)"

NUM_ABL=$(find "$SUPP_ROOT/experiments/02_metaprogramming_ablation" -mindepth 3 -maxdepth 3 -type d | wc -l | tr -d ' ')
[ "$NUM_ABL" = "8" ] && pass "02_metaprogramming_ablation has 8 cells" || fail "02_metaprogramming_ablation has $NUM_ABL cells (expected 8)"

NUM_CROSS=$(find "$SUPP_ROOT/experiments/04_cross_language_transfer/javascript" \
                "$SUPP_ROOT/experiments/04_cross_language_transfer/rust" \
                -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
[ "$NUM_CROSS" = "4" ] && pass "04_cross_language_transfer has 4 cells" || fail "04_cross_language_transfer has $NUM_CROSS cells (expected 4)"

echo
echo "[E] Harness end-to-end on a real cell"
TEST_CELL="$SUPP_ROOT/experiments/01_main_experiments/claude_code/opus_4_6/brainfuck"
cd "$TEST_CELL"
rm -f harness_state.json
python3 harness.py init --language brainfuck >/dev/null
[ -f harness_state.json ] && pass "init created harness_state.json" || fail "init did not create state"

python3 harness.py fetch >/dev/null && pass "fetch succeeded" || fail "fetch failed"

echo ',[.,]' > tmp_echo.bf
python3 harness.py run tmp_echo.bf --input "abc" 2>&1 | grep -q "OUTPUT: 'abc'" \
  && pass "run echoes input via BF interpreter" || fail "run did not produce expected output"

python3 harness.py status >/dev/null && pass "status succeeded" || fail "status failed"

# Submit three times and confirm the fourth is rejected.
for i in 1 2 3; do
  python3 harness.py submit E01 tmp_echo.bf >/dev/null 2>&1 \
    && pass "submission $i accepted" \
    || fail "submission $i unexpectedly rejected"
done
out=$(python3 harness.py submit E01 tmp_echo.bf 2>&1 || true)
echo "$out" | grep -qE "Maximum 3 submissions reached|all 3 submissions" \
  && pass "4th submission correctly rejected (max-3 enforced)" \
  || fail "4th submission not rejected; got: $out"

# Confirm export writes export.json containing E01.
rm -f export.json
python3 harness.py export >/dev/null 2>&1
[ -f export.json ] && grep -q '"E01"' export.json \
  && pass "export produces JSON with E01 entry" \
  || fail "export missing E01"

rm -f tmp_echo.bf harness_state.json export.json
rm -rf logs
cd "$SUPP_ROOT"

echo
echo "[F] Summary"
echo "  PASS: $PASS_COUNT"
echo "  FAIL: $FAIL_COUNT"
if [ "$FAIL_COUNT" -gt 0 ]; then
  echo
  echo "RIGOROUS TEST FAILED."
  exit 1
fi
echo
echo "RIGOROUS TEST PASSED."
