#!/usr/bin/env bash
# Wire up every experiment under supplementary_code/experiments/.
# Idempotent: reruns recreate cell directories with `--force`.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUPP_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "[1/5] Setting up main-experiment grid (24 cells: 6 agents x 4 languages)"
python3 "$SCRIPT_DIR/setup_main_grid.py"

echo "[2/5] Setting up metaprogramming-ablation cells"
python3 "$SUPP_ROOT/experiments/02_metaprogramming_ablation/setup_cells.py" --force

echo "[3/5] Setting up distillation cells (text + library)"
python3 "$SUPP_ROOT/experiments/03_distillation/setup_cells.py" --force

echo "[4/5] Setting up cross-language-transfer cells"
python3 "$SUPP_ROOT/experiments/04_cross_language_transfer/setup_cells.py"

echo "[5/5] Validating ablation cells"
python3 "$SUPP_ROOT/experiments/02_metaprogramming_ablation/validate_cells.py"

echo
echo "All cells set up. Each cell has:"
echo "  - harness.py (symlink to shared $SUPP_ROOT/benchmark_harness/harness.py)"
echo "  - CLAUDE.md / AGENTS.md (per-condition prompt + language-reference card)"
echo
echo "Initialize a cell with:"
echo "  cd <cell_dir>"
echo "  python harness.py init --language <brainfuck|befunge-98|whitespace|shakespeare>"
