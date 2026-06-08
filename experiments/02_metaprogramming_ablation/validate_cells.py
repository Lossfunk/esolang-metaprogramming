#!/usr/bin/env python3
"""Validate that ablation cells under this directory are wired correctly."""

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SUPP_ROOT = SCRIPT_DIR.parent.parent
HARNESS_PATH = (SUPP_ROOT / "benchmark_harness" / "harness.py").resolve()

CONDITIONS = ("meta_allowed", "meta_forbidden")
MODELS = ("opus_4_6", "gpt_5_4_xhigh")
LANGUAGES = ("brainfuck", "befunge98")

errors: list[str] = []
checked = 0

for cond in CONDITIONS:
    for model in MODELS:
        for lang in LANGUAGES:
            cell = SCRIPT_DIR / cond / model / lang
            checked += 1
            if not cell.is_dir():
                errors.append(f"missing cell directory: {cell}")
                continue
            harness = cell / "harness.py"
            if not harness.exists():
                errors.append(f"missing harness.py in {cell}")
            elif harness.is_symlink() and harness.resolve() != HARNESS_PATH:
                errors.append(
                    f"harness.py in {cell} points to {harness.resolve()}, "
                    f"expected {HARNESS_PATH}"
                )
            for prompt_name in ("CLAUDE.md", "AGENTS.md"):
                p = cell / prompt_name
                if not p.exists() or p.stat().st_size == 0:
                    errors.append(f"missing or empty {prompt_name} in {cell}")

if errors:
    print(f"FAIL - {len(errors)} of {checked} cells have issues:\n")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK - all {checked} ablation cells are wired correctly.")
