#!/usr/bin/env python3
"""Build the pi benchmark cells:

    experiments/01_main_experiments/pi/<language>/
        harness.py   -> symlink to benchmark_harness/harness.py
        AGENTS.md    -> symlink to prompts/<language>/AGENTS.md

Mirrors scripts/setup_main_grid.py's pattern, but there's no per-model
subdirectory -- for pi, the model is a `pi/run_cell.sh --model` runtime flag,
not a fixed cell (that's how the operator's own config, not a pinned
checkpoint, is what's under test).

Idempotent: safe to re-run.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PI_DIR = Path(__file__).resolve().parent
REPO_ROOT = PI_DIR.parent
EXPT_ROOT = REPO_ROOT / "experiments" / "01_main_experiments" / "pi"
HARNESS_PATH = (REPO_ROOT / "benchmark_harness" / "harness.py").resolve()
PROMPTS_DIR = REPO_ROOT / "prompts"

# (cell_dirname, prompts_subdir) -- cell_dirname matches --language values
# used elsewhere in the repo; prompts_subdir matches the actual prompts/ tree
# (which drops the hyphen for befunge-98 -> befunge98).
LANGS = [
    ("brainfuck", "brainfuck"),
    ("befunge-98", "befunge98"),
    ("whitespace", "whitespace"),
    ("shakespeare", "shakespeare"),
]


def link(src: Path, dst: Path) -> None:
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    rel = os.path.relpath(src, dst.parent)
    dst.symlink_to(rel)


def main() -> int:
    if not HARNESS_PATH.exists():
        print(f"ERROR: harness not found at {HARNESS_PATH}", file=sys.stderr)
        return 1

    built = 0
    for lang_dirname, prompts_subdir in LANGS:
        prompt_src = (PROMPTS_DIR / prompts_subdir / "AGENTS.md").resolve()
        if not prompt_src.exists():
            print(f"ERROR: prompt not found at {prompt_src}", file=sys.stderr)
            return 1

        cell = EXPT_ROOT / lang_dirname
        cell.mkdir(parents=True, exist_ok=True)
        link(HARNESS_PATH, cell / "harness.py")
        link(prompt_src, cell / "AGENTS.md")
        print(f"  built  pi/{lang_dirname}")
        built += 1

    print()
    print(f"Built {built} pi cells under {EXPT_ROOT}")
    print()
    print("Run a cell (real dataset must be loaded first via pi/load_dataset.py):")
    print(f"  pi/run_cell.sh --model <id> --language <brainfuck|befunge-98|whitespace|shakespeare>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
