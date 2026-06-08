# Main Experiments — 4 Esolangs × 6 Agents

This is the headline EsoLang-Bench evaluation reported in Section 3.1 of the
paper (Table 1 and Figure 3).

## What this evaluates

Six contemporary LLM-based coding agents on four esoteric programming languages
under a common agentic protocol:

| Model | Native harness |
|---|---|
| Claude Opus 4.6 | Claude Code |
| Claude Sonnet 4.6 | Claude Code |
| Claude Haiku 4.5 | Claude Code |
| GPT-5.4 xhigh | Codex |
| GPT-5.4 mini | Codex |
| Kimi K2.5 | OpenCode |

## Protocol parameters (held constant across all 24 cells)

- 80 problems per language, fetched in fixed forward order (E01–X20).
- Up to 3 hidden-test submissions per problem.
- **Unlimited** local interpreter calls (`python harness.py run …`).
- Six private hidden tests per problem; only an aggregate pass count is returned
  to the agent.
- A problem is solved iff one submission passes all six hidden tests.

## How a cell is wired

A *cell* is one (model × language) run. Each cell is a directory containing:

- `harness.py` — the benchmark harness (one shared copy in `../../benchmark_harness/`).
- `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex, OpenCode) — the
  per-language language-reference prompt copied from `../../prompts/<lang>/`.
- `harness_state.json` — auto-created on first `init`.
- A workspace where the agent edits files.

## Set up a single cell

From the supplementary code root:

```bash
# Pick a model and language, then create a cell directory.
mkdir -p experiments/01_main_experiments/<model>/<lang>
cd experiments/01_main_experiments/<model>/<lang>

# Symlink the shared harness and the matching language-reference prompt.
ln -s ../../../../benchmark_harness/harness.py harness.py
ln -s ../../../../prompts/<lang>/CLAUDE.md CLAUDE.md   # for Claude Code
# ln -s ../../../../prompts/<lang>/AGENTS.md AGENTS.md  # for Codex / OpenCode

# Initialize the cell.
python harness.py init --language <lang>
```

The valid language values are `brainfuck`, `befunge-98`, `whitespace`,
`shakespeare`.

## Run the agent

The agent reads `CLAUDE.md` (or `AGENTS.md`) and starts with `fetch`. The
harness commands it has are:

```
python harness.py fetch                          # next problem
python harness.py run <code_file> --input "…"    # local interpreter (unlimited)
python harness.py submit <problem_id> <file>     # hidden eval (max 3 per problem)
python harness.py status                         # progress dashboard
python harness.py skip                           # skip ONLY after attempting
python harness.py export                         # full state JSON
```

Concrete launch commands per harness:

```bash
# Claude Code (Anthropic)
claude --no-alt-screen --model claude-opus-4-6 \
  "Read CLAUDE.md and follow it exactly. Start with python harness.py fetch."

# Codex (OpenAI)
codex --no-alt-screen -m gpt-5.4 -c model_reasoning_effort=xhigh \
  -a never -s workspace-write \
  "Read AGENTS.md and follow it exactly. Start with python harness.py fetch."

# OpenCode (Moonshot, third-party wrapper)
opencode -m kimi-k2-5 \
  "Read AGENTS.md and follow it exactly. Start with python harness.py fetch."
```

(Replace model identifiers with your provider's current values.)

## Re-create the entire 4×6 grid in one shot

```bash
cd ../../scripts
python3 setup_main_grid.py   # creates 4 langs × 6 models = 24 cells, ready to run
```

## What gets reported

After a session ends, `python harness.py status` shows the cell's solved count
out of 80. The `export` command emits a JSON of every fetch / run / submit
event with timestamps and submission contents — this is the per-cell record
behind Table 1 and Figure 3 in the paper.
