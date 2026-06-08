#!/usr/bin/env python3
"""Wire up the cross-language-transfer cells in the supplementary layout.

Each cell already has its AGENTS.md and CLAUDE.md (the host-language
constraint plus the standard language-reference card). This script
symlinks the shared harness.py into each cell so the harness commands
work out of the box.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SUPP_ROOT = SCRIPT_DIR.parent.parent
HARNESS_PATH = (SUPP_ROOT / "benchmark_harness" / "harness.py").resolve()

CELLS = [
    ("javascript", "brainfuck"),
    ("javascript", "befunge98"),
    ("rust",       "brainfuck"),
    ("rust",       "befunge98"),
]


def link_harness(cell_dir: Path) -> None:
    target = cell_dir / "harness.py"
    if target.exists() or target.is_symlink():
        target.unlink()
    rel = os.path.relpath(HARNESS_PATH, target.parent)
    target.symlink_to(rel)


def main() -> int:
    if not HARNESS_PATH.exists():
        print(f"ERROR: harness not found at {HARNESS_PATH}")
        return 1
    for host, lang in CELLS:
        cell = SCRIPT_DIR / host / lang
        cell.mkdir(parents=True, exist_ok=True)
        link_harness(cell)
        print(f"  linked harness in {cell.relative_to(SCRIPT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
