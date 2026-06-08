# EsoLang-Bench Meta-Programming Ablation

You are solving 80 programming problems in **{LANGUAGE_DISPLAY}** through a
local evaluation harness.

This workspace belongs to the paper's **meta-programming forbidden** ablation
condition.

## Read First

- `docs/{LANGUAGE_DOC}`

## Evaluation Policy

- **Local interpreter calls are unbounded**
- Every `python harness.py run <file> --input "..."` is allowed
- **Maximum 1 hidden-test submission per problem**
- The single `submit` is blind and final for that problem

## Condition: Direct Authoring Only

- You must write solution code directly in **{LANGUAGE_DISPLAY}**.
- Do not write or run Python, JavaScript, Rust, C/C++, Perl, awk, sed scripts,
  shell loops, shell arithmetic, or any other helper program to generate,
  assemble, transform, layout, optimize, or verify **{LANGUAGE_DISPLAY}**
  solution files.
- Do not use helper code to compute constants, expected outputs, routing
  tables, layouts, test oracles, reference answers, or intermediate artifacts.
- Do not use shell pipelines, text-processing scripts, template emitters, or
  command substitutions to produce or modify **{LANGUAGE_DISPLAY}** code.
- Shell usage is limited to basic workspace operations and the harness commands
  listed below. It must not perform algorithmic processing for the solution.
- All implementation, debugging, and verification must be based on direct
  **{LANGUAGE_DISPLAY}** code plus `python harness.py run` outputs. Reason
  manually from the public problem statement and the target-language behavior.

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
