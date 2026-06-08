# Cross-Language Transfer (Section 3.2 of the paper, Table 4)

This is the experiment that asks whether the metaprogramming benefit
is *Python-specific* or transfers to other host languages.

## What this evaluates

For GPT-5.4 xhigh on the two diagnostic languages (Brainfuck and
Befunge-98), we re-run the metaprogramming-allowed condition under
three host-language constraints:

| Host language | Allowed solver path |
|---|---|
| Python (default) | Python generator emits the target esolang. |
| JavaScript       | JavaScript / Node.js generator emits the target esolang. |
| Rust             | Rust generator emits the target esolang. |
| Direct (control) | No host-language generator; author target esolang directly. |

The Python row is the headline number from Table 1; the JavaScript,
Rust, and Direct rows are reported in Table 4.

## Cell layout

```
04_cross_language_transfer/
  javascript/
    brainfuck/   AGENTS.md, CLAUDE.md, harness.py
    befunge98/   AGENTS.md, CLAUDE.md, harness.py
  rust/
    brainfuck/   AGENTS.md, CLAUDE.md, harness.py
    befunge98/   AGENTS.md, CLAUDE.md, harness.py
```

The Python row reuses the `01_main_experiments` GPT-5.4 xhigh cells
on Brainfuck and Befunge-98 (no separate folder needed).
The Direct row reuses the `02_metaprogramming_ablation/meta_forbidden`
GPT-5.4 xhigh cells on the same two languages.

## Build the cells

```bash
cd experiments/04_cross_language_transfer
python setup_cells.py --force
```

The setup script symlinks `harness.py` from `../../benchmark_harness/`
into each of the four cells. The `AGENTS.md` and `CLAUDE.md` files are
already in place; they each carry the host-language constraint at
the top (e.g., *"You MUST write JavaScript/Node.js helper scripts that
generate, assemble, or transform Brainfuck programs"*) followed by
the standard language-reference card.

## Initialize and run a single cell

```bash
cd javascript/brainfuck
python harness.py init --language brainfuck

# Then launch the agent reading AGENTS.md.
codex --no-alt-screen -m gpt-5.4 -c model_reasoning_effort=xhigh \
  -a never -s workspace-write \
  "Read AGENTS.md and follow it exactly. Start with python harness.py fetch."
```

## What gets reported

Each cell produces a per-cell solved count out of 80. The headline
row in Table 4 (*The metaprogramming benefit transfers across host
languages*) compares Python / JavaScript / Rust / Direct. The
side-by-side E04 generator excerpts are shown in Appendix B.4
(`app:cross-language-code`).
