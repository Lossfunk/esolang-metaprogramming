# EsoLang-Bench Cross-Language Meta-Programming: JavaScript -> Brainfuck

You are solving 80 programming problems in **Brainfuck** through a local
evaluation harness.

This workspace is a GPT-5.4 xhigh cross-language transfer ablation. The purpose
is to test whether meta-programming still works when the generator language is
**JavaScript** rather than Python.

## Read First

- `docs/brainfuck_reference.md`

## Evaluation Policy

- **Local interpreter calls are unbounded**
- Every `python harness.py run <file> --input "..."` is allowed
- **Maximum 1 hidden-test submission per problem**
- The single `submit` is blind and final for that problem

## Critical Condition: JavaScript-Only Meta-Programming

- You MUST write JavaScript/Node.js helper scripts that generate, assemble, or
  transform Brainfuck programs.
- You may use JavaScript for generator libraries, emitters, templates, and
  compiler-style workflows.
- The final submitted file must still be a **Brainfuck** program.
- You may keep JavaScript helper scripts and generated artifacts inside this
  workspace.
- You may NOT use Python, Rust, C/C++, shell scripts, or any other language to
  generate Brainfuck.
- You may NOT write final Brainfuck by hand as the primary workflow. Brainfuck
  should be emitted by JavaScript.

Recommended workflow:

```bash
node gen_E01.js > solutions/E01.bf
python harness.py run solutions/E01.bf --input "..."
python harness.py submit E01 solutions/E01.bf
```

## Harness Commands

```bash
python harness.py init --language brainfuck --budget inf
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

This session should already be initialized. Start with:

```bash
python harness.py fetch
```

