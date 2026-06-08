#!/usr/bin/env python3
"""Generate metaprogramming-ablation cells under the supplementary layout.

Each cell becomes:

    02_metaprogramming_ablation/<condition>/<model>/<language>/
        harness.py            -> symlink to benchmark_harness/harness.py
        CLAUDE.md             -> condition prompt + language reference
        AGENTS.md             -> same content (Codex / OpenCode)
        harness_state.json    -> created on first `python harness.py init`

Conditions:
    meta_allowed     : agent may use a host-language generator (Python, etc.)
    meta_forbidden   : harness blocks bash; agent must author target esolang directly

Languages:    brainfuck, befunge98 (the two diagnostic languages)
Models:       opus_4_6, gpt_5_4_xhigh (the two strongest agents)
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SUPP_ROOT = SCRIPT_DIR.parent.parent
HARNESS_PATH = SUPP_ROOT / "benchmark_harness" / "harness.py"
LANG_PROMPT_DIR = SUPP_ROOT / "prompts"

PROMPT_ALLOWED = SCRIPT_DIR / "PROMPT_META_ALLOWED.md"
PROMPT_FORBIDDEN = SCRIPT_DIR / "PROMPT_META_FORBIDDEN.md"

MODELS = ["opus_4_6", "gpt_5_4_xhigh"]
LANGUAGES = ["brainfuck", "befunge98"]
CONDITIONS = {
    "meta_allowed": PROMPT_ALLOWED,
    "meta_forbidden": PROMPT_FORBIDDEN,
}

LANG_INIT = {
    "brainfuck": "brainfuck",
    "befunge98": "befunge-98",
}


def write_prompt(cell_dir: Path, condition_prompt: Path, language: str) -> None:
    """Write CLAUDE.md and AGENTS.md = condition prompt + language reference."""
    condition_text = condition_prompt.read_text()
    lang_card = (LANG_PROMPT_DIR / language / "CLAUDE.md").read_text()
    full = condition_text.rstrip() + "\n\n---\n\n" + lang_card
    (cell_dir / "CLAUDE.md").write_text(full)
    (cell_dir / "AGENTS.md").write_text(full)


def link_harness(cell_dir: Path) -> None:
    target = cell_dir / "harness.py"
    if target.exists() or target.is_symlink():
        target.unlink()
    rel = os.path.relpath(HARNESS_PATH.resolve(), target.parent)
    target.symlink_to(rel)


def build_cell(condition: str, model: str, language: str, force: bool) -> Path:
    cell = SCRIPT_DIR / condition / model / language
    if cell.exists() and force:
        shutil.rmtree(cell)
    cell.mkdir(parents=True, exist_ok=True)
    link_harness(cell)
    write_prompt(cell, CONDITIONS[condition], language)
    return cell


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--force", action="store_true",
                        help="Wipe existing cell directories before recreating.")
    args = parser.parse_args()

    if not HARNESS_PATH.exists():
        print(f"ERROR: harness not found at {HARNESS_PATH}")
        return 1

    print(f"Supplementary root: {SUPP_ROOT}")
    print(f"Harness:            {HARNESS_PATH}")
    for condition in CONDITIONS:
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
