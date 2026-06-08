#!/usr/bin/env python3
"""Build the 4-language x 6-agent main-experiment grid as cell directories.

Each cell becomes:

    experiments/01_main_experiments/<harness>/<model>/<language>/
        harness.py            -> symlink to benchmark_harness/harness.py
        CLAUDE.md (Claude Code) or AGENTS.md (Codex / OpenCode)
                              -> symlink to prompts/<language>/...

24 cells total: 6 (model x harness) x 4 languages.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SUPP_ROOT = SCRIPT_DIR.parent
EXPT_ROOT = SUPP_ROOT / "experiments" / "01_main_experiments"
HARNESS_PATH = (SUPP_ROOT / "benchmark_harness" / "harness.py").resolve()
PROMPTS_DIR = SUPP_ROOT / "prompts"

LANGS = ["brainfuck", "befunge98", "whitespace", "shakespeare"]

# (harness_subdir, model_subdir, prompt_filename)
CELLS = [
    ("claude_code", "opus_4_6",       "CLAUDE.md"),
    ("claude_code", "sonnet_4_6",     "CLAUDE.md"),
    ("claude_code", "haiku_4_5",      "CLAUDE.md"),
    ("codex",       "gpt_5_4_xhigh",  "AGENTS.md"),
    ("codex",       "gpt_5_4_mini",   "AGENTS.md"),
    ("opencode",    "kimi_k2_5",      "AGENTS.md"),
]


def link(src: Path, dst: Path) -> None:
    """Symlink dst -> src using a path relative to dst's parent.

    Relative targets keep the supplementary tree portable and prevent the
    author's absolute home path from leaking through the symlink target
    (which would break double-blind anonymity).
    """
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    rel = os.path.relpath(src, dst.parent)
    dst.symlink_to(rel)


def main() -> int:
    if not HARNESS_PATH.exists():
        print(f"ERROR: harness not found at {HARNESS_PATH}", file=sys.stderr)
        return 1

    built = 0
    for harness_subdir, model, prompt_name in CELLS:
        for lang in LANGS:
            cell = EXPT_ROOT / harness_subdir / model / lang
            cell.mkdir(parents=True, exist_ok=True)
            link(HARNESS_PATH, cell / "harness.py")
            prompt_src = (PROMPTS_DIR / lang / prompt_name).resolve()
            link(prompt_src, cell / prompt_name)
            print(f"  built  {harness_subdir}/{model}/{lang}")
            built += 1

    print()
    print(f"Built {built} main-experiment cells.")
    print()
    print("Initialize a cell:")
    print(f"  cd {EXPT_ROOT}/<harness>/<model>/<lang>")
    print( "  python harness.py init --language <brainfuck|befunge-98|whitespace|shakespeare>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
