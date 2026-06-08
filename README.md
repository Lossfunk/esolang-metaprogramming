# Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages

Official code release for the paper
**Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages**
Aman Sharma, Sushrut Thorat, Paras Chopra · **Lossfunk** · 2026.

- 📄 Paper / preprint: see the project page
- 🌐 Project page: **https://lossfunk.com** (metaprogramming paper)
- 🤗 Benchmark dataset (EsoLang-Bench): **https://huggingface.co/datasets/Lossfunk/Esolang-Bench**

This repository lets you **reproduce every result in the paper** and, more
importantly, **run the whole evaluation yourself** with whatever coding-agent
plan you already have — Claude Code, Codex, OpenCode, or any model through
OpenRouter.

It contains:

- the evaluation **harness** for EsoLang-Bench (a previously released,
  third-party benchmark — see "Dataset" below; this work *consumes* the
  benchmark, it does not introduce it);
- the four esoteric-language **interpreters** (Brainfuck, Befunge-98,
  Whitespace, Shakespeare);
- the **public problem statements** and a structure-preserving, answer-redacted
  copy of the hidden tests (download the real hidden tests from the dataset
  page to grade end-to-end — see "Dataset");
- the per-language **agent prompts** (`CLAUDE.md` for Claude Code, `AGENTS.md`
  for Codex / OpenCode — identical content);
- the **experiment configurations**: main grid, metaprogramming ablation, and
  cross-language transfer.

---

## TL;DR — run one cell in 60 seconds

```bash
# 0. clone + enter
git clone https://github.com/lossfunk/esolang-metaprogramming.git
cd esolang-metaprogramming

# 1. environment (harness needs only Python 3.10+; one pkg for Shakespeare)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. confirm the harness works with NO API key (smoke test)
bash scripts/test_harness.sh

# 3. build all experiment cells
bash scripts/setup_all.sh

# 4. initialize one cell and point your agent at it
cd experiments/01_main_experiments/claude_code/opus_4_6/brainfuck
python harness.py init --language brainfuck
claude --model claude-opus-4-6 \
  "Read CLAUDE.md and follow it exactly. Begin with: python harness.py fetch."
```

The harness is just five local commands the agent calls (`init`, `fetch`,
`run`, `submit`, `status`). It needs **no API key** — only the agent wrapper
that drives it does. See **[HOWTO_RUN.md](HOWTO_RUN.md)** for every provider.

---

## Run it with your own plan

You can drive the harness with any agent CLI. Pick the row that matches the
plan you have. **The easiest "run every model in the paper with one key" path
is OpenCode + OpenRouter.**

| Your plan | CLI | Auth | Notes |
|---|---|---|---|
| **Anthropic** (Claude) | `claude` (Claude Code) | `ANTHROPIC_API_KEY` | Primary harness for the Claude family in the paper |
| **OpenAI** (GPT) | `codex` (Codex CLI) | `OPENAI_API_KEY` | Primary harness for the GPT-5.4 family |
| **OpenRouter** (any model) | `opencode` | `OPENROUTER_API_KEY` | One key → Claude, GPT, Kimi, Llama, … (recommended for full reproduction) |
| **Moonshot** (Kimi) | `opencode` | per OpenCode docs | Kimi K2.5 cell in the paper |

Each agent reads `CLAUDE.md`/`AGENTS.md` from the cell, then issues the same
five harness commands. The benchmark is provider-agnostic — only the wrapper
changes. Full per-provider commands (including **how to point each CLI at
OpenRouter**) are in **[HOWTO_RUN.md](HOWTO_RUN.md)**.

### One key, every model (OpenRouter + OpenCode)

```bash
export OPENROUTER_API_KEY=sk-or-...
cd experiments/01_main_experiments/opencode/kimi_k2_5/brainfuck
python harness.py init --language brainfuck
# select any OpenRouter model id, e.g. anthropic/claude-opus-4, openai/gpt-5,
# moonshotai/kimi-k2 — see HOWTO_RUN.md for opencode provider config
opencode -m openrouter/anthropic/claude-opus-4 \
  "Read AGENTS.md and follow it exactly. Begin with python harness.py fetch."
```

---

## Layout

```
esolang-metaprogramming/
  benchmark_harness/             ONE shared harness + interpreters + data
    harness.py                   the harness every cell calls
    interpreters/                Brainfuck, Befunge-98, Whitespace, Shakespeare
    public/esolang_full_public.json    public problem statements
    private/esolang_full_private.json  hidden tests, REDACTED here (see Dataset)
  prompts/                       per-language reference prompt
    {brainfuck,befunge98,whitespace,shakespeare}/{CLAUDE.md,AGENTS.md}
  experiments/
    01_main_experiments/         6 agents x 4 languages   (Table 1, Figure 3)
    02_metaprogramming_ablation/ meta-allowed vs forbidden (Section 3.2, Figure 4)
    04_cross_language_transfer/  Python / JS / Rust gens   (Table 4)
  scripts/
    setup_all.sh                 wire up every experiment in one shot
    setup_main_grid.py           build the 6-agent x 4-language main grid
    test_harness.sh              smoke test (no provider API calls)
    rigorous_test.sh             extended end-to-end test
  HOWTO_RUN.md                   per-provider run instructions (Claude / Codex / OpenCode / OpenRouter)
  CITATION.cff                   how to cite this work
  requirements.txt  LICENSE
```

## Protocol (held constant across every experiment unless noted)

- 80 problems per language (E01–X20, fixed forward order).
- **Up to 3 hidden-test submissions per problem** (`MAX_SUBMISSIONS = 3` in `harness.py`).
- **Unlimited** local interpreter calls (`python harness.py run …`).
- **6 private hidden tests per problem**; only an aggregate pass/total count is
  returned. A problem is solved iff one submission returns 6/6.

## What lives where in the paper

| Paper section / table | Reproduced from |
|---|---|
| Table 1, Figure 3 (capability cliff) | `experiments/01_main_experiments/` |
| Figure 4 (meta-allowed vs forbidden) | `experiments/02_metaprogramming_ablation/` |
| Table 4 (cross-language) | `experiments/04_cross_language_transfer/` |
| Appendix B (raw counts, CIs) | per-cell `export.json` under `01_main_experiments/` |
| Appendix B.8 (cross-harness) | `experiments/01_main_experiments/{codex,opencode}/` |

## Dataset (third-party)

EsoLang-Bench is a **previously released, third-party benchmark** that this
paper consumes; it is not introduced here.

- Dataset card: **https://huggingface.co/datasets/Lossfunk/Esolang-Bench**

The hidden tests in `benchmark_harness/private/esolang_full_private.json` are
**redacted** in this repo — every test input and expected output is replaced by
a marker string, so the JSON structure is visible but the answers are not.
Bundling them would compromise the benchmark for everyone. To grade end to end
and reproduce the headline numbers:

1. Download the unredacted private file from the dataset page above.
2. Overwrite `benchmark_harness/private/esolang_full_private.json` with it (the
   schema already matches).
3. Re-run `bash scripts/test_harness.sh` to confirm.

Without step 2 the harness still runs end to end, but every `submit` returns
`WRONG ANSWER` because the answers are masked — which is exactly what the smoke
test exercises.

## License and authorship

The harness, interpreters, and per-language prompts are released under the MIT
License (see `LICENSE`). The EsoLang-Bench dataset is a separately released
artifact; its license is set by the dataset maintainers on the HuggingFace page
above.

## Citation

See **[CITATION.cff](CITATION.cff)**, or:

```bibtex
@misc{sharma2026metaprogramming,
  title  = {Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages},
  author = {Sharma, Aman and Thorat, Sushrut and Chopra, Paras},
  year   = {2026},
  note   = {Lossfunk},
  url    = {https://lossfunk.com}
}
```
