# EsoLang-Bench NeurIPS Meta-Programming Ablation

You are solving 80 programming problems in **{LANGUAGE_DISPLAY}** through a
local evaluation harness.

This workspace belongs to the paper's **meta-programming allowed** ablation
condition.

## Read First

- `docs/{LANGUAGE_DOC}`

## Evaluation Policy

- **Local interpreter calls are unbounded**
- Every `python harness.py run <file> --input "..."` is allowed
- **Maximum 1 hidden-test submission per problem**
- The single `submit` is blind and final for that problem

## Condition: Meta-Programming Allowed

- You may write Python helper scripts that generate, assemble, or transform
  **{LANGUAGE_DISPLAY}** programs.
- For hard and extra-hard problems, prefer generator-based or compiler-style
  workflows when they help.
- The final submitted file must still be a **{LANGUAGE_DISPLAY}** program.
- You may keep Python helper scripts and intermediate build artifacts inside
  this workspace.

## Harness Commands

```bash
python harness.py init --language {INIT_LANGUAGE} --budget inf
python harness.py fetch
python harness.py run <code_file> --input "..."
python harness.py submit <problem_id> <file>
python harness.py status
python harness.py export
```

## Rules

- Solve problems in order. `fetch` gives the next problem only when the current
  one is finished.
- Generate your own tests from the public description.
- Work only inside this workspace and its local `docs/` folder.
- Do not read or copy files from parent directories, sibling benchmark cells,
  other experiment folders, transcripts, logs, or prior solution directories.
- Do not inspect `harness.py`, interpreter implementation files, or any
  benchmark-private data for solution content.
- Do not read private tests or any file under a `private/` directory.
- Do not modify `harness.py`, interpreter modules, or `harness_state.json`.
- Do not use web search or network tools.

## Start

Run:

```bash
python harness.py init --language {INIT_LANGUAGE} --budget inf
python harness.py fetch
```
