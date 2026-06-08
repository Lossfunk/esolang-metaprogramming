# Metaprogramming Ablation (Section 3.2 of the paper)

This is the diagnostic experiment that asks whether metaprogramming
*causes* the headline performance of the strongest agents on
Brainfuck and Befunge-98, or merely correlates with it.

## What this evaluates

For the two strongest agents (Claude Opus 4.6 and GPT-5.4 xhigh) on the
two diagnostic languages (Brainfuck and Befunge-98), we run two
conditions:

| Condition | Bash access | Allowed solver path | Question answered |
|---|---|---|---|
| `meta_allowed` | yes | host-language generator OR direct authoring | Free-choice baseline. |
| `meta_forbidden` | no | direct authoring of target esolang only | What if metaprogramming is removed? |

The two conditions share everything else: same EsoLang-Bench problems,
same hidden tests, same 3-submission cap, same unlimited local
interpreter access, same per-language reference card. The only
differences are (a) the harness removes the agent's bash access in
`meta_forbidden`, and (b) the system-prompt preamble is swapped.

## Cell layout (after running `setup_cells.py`)

```
02_metaprogramming_ablation/
  meta_allowed/
    opus_4_6/{brainfuck,befunge98}/
    gpt_5_4_xhigh/{brainfuck,befunge98}/
  meta_forbidden/
    opus_4_6/{brainfuck,befunge98}/
    gpt_5_4_xhigh/{brainfuck,befunge98}/
```

Each cell directory contains:
- `harness.py` — symlink to `../../../../benchmark_harness/harness.py`
- `CLAUDE.md` — condition preamble + language reference card
- `AGENTS.md` — identical content for Codex / OpenCode

## Build the cells

```bash
cd experiments/02_metaprogramming_ablation
python setup_cells.py --force
```

This populates 8 cells (2 conditions × 2 models × 2 languages).

## Initialize and run a single cell

```bash
cd meta_allowed/opus_4_6/brainfuck
python harness.py init --language brainfuck

# Then launch the agent reading CLAUDE.md.
claude --no-alt-screen --model claude-opus-4-6 \
  "Read CLAUDE.md and follow it exactly. Start with python harness.py fetch."
```

For `meta_forbidden` cells, the harness blocks bash; the agent must
edit `.bf` / `.b98` files directly.

## Validate that cells were built correctly

```bash
python validate_cells.py
```

## What gets reported

Each cell produces a per-cell solved count out of 80. The deltas
between `meta_allowed` and `meta_forbidden` are reported in the body
of the paper (Figure 4 — *Forcing direct authoring sharply reduces
performance on Brainfuck and Befunge-98*) and in
Appendix B.7 (`app:meta-table`).
