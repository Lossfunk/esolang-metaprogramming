# Distillation (Section 3.3 of the paper)

This is the strategy-transfer experiment. Using Claude Opus 4.6 as
the *advisor*, we transfer its strategy to three lower-performing
agents (Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4 mini) in two
forms:

| Condition | What the agent receives |
|---|---|
| `+text`    | A short system-prompt preamble summarising the strategy (use a generator, build reusable primitives, verify locally, regenerate components rather than hand-patching target code). |
| `+library` | The text preamble *plus* a small reference library of working host-language helper files (the contents of `reference_lib/<lang>/` here). |

The two diagnostic languages are Brainfuck and Befunge-98.

## Critical: this is a *library-only* release

The experimental contrast is whether weaker agents can **build**
working generators from reusable scaffolding (the library) versus
following written advice alone (the text). It is **not** about
whether they can copy finished solutions.

For that reason, no per-problem generator files and no solved
target-language artifacts from the original distillation workspaces
are shipped. Only the general strategy library — reusable code-
generation helpers, builder patterns, learning notes, and a Befunge-98
simulator — is shipped, in `reference_lib/brainfuck/` and
`reference_lib/befunge98/`. The exact file listing for each language
is in that directory's own `README.md`.

## Layout

```
03_distillation/
  README.md                  (this file)
  prompts/
    PROMPT_BRAINFUCK.md      Distilled-strategy preamble for Brainfuck.
    PROMPT_BEFUNGE98.md      Distilled-strategy preamble for Befunge-98.
    REF_BRAINFUCK_README.md  Allowed/not-allowed framing for the +library cell.
    REF_BEFUNGE98_README.md  Same, for Befunge-98.
  reference_lib/
    brainfuck/               Library files only (no per-problem generators).
    befunge98/               Library files only (no per-problem generators).
  setup_cells.py             Builds the per-model+per-language cells.
```

## Build the cells

```bash
cd experiments/03_distillation
python setup_cells.py --condition library --force   # +library cells
python setup_cells.py --condition text    --force   # +text cells
```

This populates 12 cells (3 weaker models × 2 languages × 2 conditions).
Each cell directory contains:

- `harness.py` — symlink to `../../../../../benchmark_harness/harness.py`
- `CLAUDE.md`  — distilled strategy preamble + language-reference card
- `AGENTS.md`  — identical content for Codex / OpenCode
- `reference_lib/`   — present only in `+library` cells; symlinked to
  `../../../../../reference_lib/<language>/`

## Initialize and run a single cell

```bash
cd library/sonnet_4_6/brainfuck
python harness.py init --language brainfuck

# Then launch the agent reading CLAUDE.md.
claude --no-alt-screen --model claude-sonnet-4-6 \
  "Read CLAUDE.md and follow it exactly. Start with python harness.py fetch."
```

## What gets reported

Each cell produces a per-cell solved count out of 80. The deltas
between baseline / `+text` / `+library` are reported in Table 5 of
the paper (Section 3.3, *Strategy transfer works through executable
scaffolds, not just written advice*) and in
Appendix B.10 (`app:distillation-prompts`).
