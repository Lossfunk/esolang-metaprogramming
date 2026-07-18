# Running EsoLang-Bench with `pi`

This adds `pi` (https://github.com/earendil-works/pi-mono, the `pi` CLI coding
agent) as a benchmark wrapper alongside the paper's `claude`/`codex`/`opencode`.

**What this measures is deliberately not "just a model."** `pi` is launched
with normal discovery on (no `--no-extensions`/`--no-skills`/`--no-context-files`),
so it loads the operator's *personal* setup — global `~/.pi/agent/AGENTS.md`
conventions, installed extensions, skills — in addition to the cell's own
`AGENTS.md` benchmark prompt (pi discovers and concatenates every `AGENTS.md`
found walking up from the working directory). The point of this toolkit is to
see how *that whole personal configuration*, not a bare model, performs on the
benchmark.

## Contents

| File | Purpose |
|---|---|
| `load_dataset.py` | Pulls the **real, unredacted** hidden tests from the `Lossfunk/Esolang-Bench` HuggingFace dataset and writes them to a git-ignored local file. **Never commit this file's output** — see Dataset below. |
| `setup_cells.py` | Builds `experiments/01_main_experiments/pi/<language>/` cells (harness + `AGENTS.md` symlinks), mirroring `scripts/setup_main_grid.py`'s pattern but without a fixed model subdirectory. |
| `run_cell.sh` | Headless driver: loops `pi -p`/session-continuation against a cell until it's finished (or a smoke cap is hit). **`--model` is a required flag — omitting it is an error, by design**, so the model under test is always a deliberate choice, never a silent default. |
| `audit.sh` | Deterministic, no-network, no-live-model-call check that everything above is wired correctly (used by the craft workflow that built this). |
| `artifacts/` | Git-ignored scratch space for run exports (e.g. smoke-test output). |

## 1. Environment setup

Same as the repo root (`HOWTO_RUN.md`), plus two extra packages this toolkit
needs for the dataset pull:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install datasets huggingface_hub
```

## 2. Get the real dataset (never committed)

```bash
python3 pi/load_dataset.py
```

This tries an **anonymous** pull of `Lossfunk/Esolang-Bench` first. If it's
gated, the script exits non-zero with instructions (accept the dataset's
terms on HuggingFace while logged in, set `HF_TOKEN`, or run
`huggingface-cli login`, then re-run).

Output goes to `benchmark_harness/private/esolang_full_private.local.json` —
**a git-ignored file, distinct from the tracked, redacted
`esolang_full_private.json`.** The tracked file is never modified. **Never
commit the `.local.json` file or any other copy of the real hidden tests** —
that would compromise the benchmark for everyone else.

## 3. Build the pi cells

```bash
python3 pi/setup_cells.py
```

Builds one cell per language under
`experiments/01_main_experiments/pi/<brainfuck|befunge-98|whitespace|shakespeare>/`.
No per-model subdirectory — the model is a runtime flag to `run_cell.sh`, not
part of the cell's identity, since what's under test is "pi as configured for
this run," not one pinned checkpoint.

## 4. Run a cell

```bash
pi/run_cell.sh --model <provider/model-id> --language brainfuck
```

`--model` is **required** — there is no default, and omitting it is a hard
error (`pi/run_cell.sh --language brainfuck` alone exits non-zero naming
`--model`). This is intentional: you must pick a model deliberately for every
run, so the number you get is never accidentally attributed to the wrong
model.

Optional flags:
- `--max-turns N` — cap on pi invocations before bailing (default 40).
- `--max-problems N` — stop once N problems have been finalized
  (solved/failed/skipped); useful for a bounded smoke test instead of the
  full 80-problem grind.
- `--dataset-file PATH` — override the private JSON (default: the
  `.local.json` from step 2).

The driver re-invokes `pi -p` against the **same session** (`--session-id`)
each turn so context carries across the run, checks `python3 harness.py
status` between turns to decide whether to continue, and finally writes
`export.json` inside the cell directory (also git-ignored).

## Comparing to the paper

To make a run comparable to a specific paper row (e.g. `claude_code/sonnet_4_6`),
pass the matching `--model`. The harness protocol (80 problems, max 3
submissions each, unlimited local `run`) is identical to every other wrapper
in the repo — only the agent driving it changes.

## Scope note

This toolkit ships the **tooling** to run pi against the benchmark, plus a
short smoke-tested proof that the wiring works end to end. It does **not**
ship a full scored 80-problem (or 4-language) run — that's a separate,
much longer job you launch yourself once you're ready to spend the tokens.
