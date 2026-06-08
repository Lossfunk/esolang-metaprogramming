#!/usr/bin/env python3
"""Generate distillation cells under the supplementary layout.

Each cell is one (condition x model x language) configuration.

Conditions:
  text     -- distilled strategy preamble only (no library on disk).
  library  -- text preamble + symlink to reference_lib/<language>/.

Models:    sonnet_4_6, haiku_4_5, gpt_5_4_mini
Languages: brainfuck, befunge98
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SUPP_ROOT = SCRIPT_DIR.parent.parent
HARNESS_PATH = (SUPP_ROOT / "benchmark_harness" / "harness.py").resolve()
LANG_PROMPT_DIR = SUPP_ROOT / "prompts"
PROMPT_DIR = SCRIPT_DIR / "prompts"
REF_LIB_DIR = SCRIPT_DIR / "reference_lib"

MODELS = ["sonnet_4_6", "haiku_4_5", "gpt_5_4_mini"]
LANGUAGES = ["brainfuck", "befunge98"]
CONDITIONS = ("text", "library")


def language_prompt_file(condition_path: Path) -> Path:
    return condition_path


def write_prompt(cell_dir: Path, language: str, condition_prompt: Path) -> None:
    text = condition_prompt.read_text()
    lang_card = (LANG_PROMPT_DIR / language / "CLAUDE.md").read_text()
    full = text.rstrip() + "\n\n---\n\n" + lang_card
    (cell_dir / "CLAUDE.md").write_text(full)
    (cell_dir / "AGENTS.md").write_text(full)


def link_harness(cell_dir: Path) -> None:
    target = cell_dir / "harness.py"
    if target.exists() or target.is_symlink():
        target.unlink()
    rel = os.path.relpath(HARNESS_PATH, target.parent)
    target.symlink_to(rel)


def link_reference_lib(cell_dir: Path, language: str) -> None:
    src = REF_LIB_DIR / language
    target = cell_dir / "reference_lib"
    if target.exists() or target.is_symlink():
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    rel = os.path.relpath(src.resolve(), target.parent)
    target.symlink_to(rel)


def build_cell(condition: str, model: str, language: str, force: bool) -> Path:
    cell = SCRIPT_DIR / condition / model / language
    if cell.exists() and force:
        shutil.rmtree(cell)
    cell.mkdir(parents=True, exist_ok=True)
    link_harness(cell)
    prompt_file = (PROMPT_DIR / f"PROMPT_{language.upper()}.md")
    write_prompt(cell, language, prompt_file)
    if condition == "library":
        link_reference_lib(cell, language)
    return cell


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--condition", choices=CONDITIONS + ("all",),
                        default="all",
                        help="Which condition(s) to set up. Default: all.")
    parser.add_argument("--force", action="store_true",
                        help="Wipe existing cell directories before recreating.")
    args = parser.parse_args()

    if not HARNESS_PATH.exists():
        print(f"ERROR: harness not found at {HARNESS_PATH}")
        return 1

    conditions = CONDITIONS if args.condition == "all" else (args.condition,)
    print(f"Supplementary root: {SUPP_ROOT}")
    print(f"Harness:            {HARNESS_PATH}")
    for condition in conditions:
        for model in MODELS:
            for language in LANGUAGES:
                cell = build_cell(condition, model, language, args.force)
                print(f"  built  {cell.relative_to(SCRIPT_DIR)}")

    print("\nNext steps:")
    print(f"  cd {SCRIPT_DIR}/<condition>/<model>/<language>")
    print(f"  python harness.py init --language <brainfuck|befunge-98>")
    print(f"  # then launch the agent reading CLAUDE.md / AGENTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
