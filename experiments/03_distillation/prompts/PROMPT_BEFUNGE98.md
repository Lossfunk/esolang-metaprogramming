# EsoLang-Bench Prompt Distillation: Befunge-98

You are solving 80 programming problems in **Befunge-98** through a local
evaluation harness.

This workspace is the paper's **prompt-distillation** condition. You are given
high-level strategies distilled from stronger successful runs, but no solved
programs, no hidden tests, and no prior generated artifacts.

## Evaluation Policy

- Local interpreter calls are unbounded.
- Use `python harness.py run <file> --input "..."` freely before submission.
- Maximum hidden-test submissions: **1 per problem**.
- The single `submit` is blind and final for that problem.
- The final submitted file must be a valid `.b98` Befunge-98 program.

## Harness Commands

```bash
python harness.py init --language befunge98 --budget inf
python harness.py fetch
python harness.py run <code_file> --input "..."
python harness.py submit <problem_id> <file>
python harness.py status
python harness.py export
```

## Integrity Rules

- Work only inside this workspace and its local `docs/` folder.
- You are explicitly allowed to read, copy, reuse, and edit files under the
  local `reference_lib/` folder.
- Do not read parent directories, sibling experiments, solution folders, logs,
  transcripts, generated files from prior runs, private tests, or any
  `private/` directory.
- Do not inspect or modify `harness.py`, interpreter modules, or
  `harness_state.json` for solution content.
- Do not use web search or network tools.
- Generate your own local tests from the problem description.

## Distilled Frontier Strategy Bundle

## Read First

Before solving any non-trivial problem, read:

- `reference_lib/README.md`
- `reference_lib/opus_simulate.py`

These are intentionally provided as local strategy scaffolds distilled from
stronger **Opus 4.6** and **GPT-5.4 xhigh** runs. They contain the local
Befunge-98 simulator and library-level patterns only — no per-problem
generators. You may read, copy, rename, edit, and extend them.

### 1. Use Python as a Befunge assembler.

For anything beyond tiny one-line programs, generate `.b98` from Python. The
Python script should manage spatial layout, not just print arbitrary strings.

Two robust architectures are allowed:

- **2D grid generator:** allocate `grid = [[" "] * WIDTH for _ in range(ROWS)]`,
  implement `put(row, col, text)`, and raise an error if a placement collides
  with existing non-space code.
- **1D label assembler:** emit linear Befunge code with labels and symbolic
  jumps, then resolve `j` offsets in Python before writing the final `.b98`.

The goal is to avoid manual routing errors.

Operational rule:

- If the program is more than a tiny one-line Befunge script, default to a
  Python generator or assembler first.

### 2. Separate code, storage, and routing.

Use a stable plan:

- Code rows for instruction-pointer routing.
- Storage rows/columns for variables accessed with `g` and `p`.
- Dedicated stack conventions for temporary values.
- Named constants for storage coordinates.
- Collision detection in generated grids.

Do not hand-place a large 2D program without a layout helper.

### 3. Pick the right I/O primitive.

Befunge-98 gives useful primitives, but formatting still matters:

- `&` reads an integer.
- `~` reads a character and returns `-1` at EOF.
- `.` prints an integer followed by a space.
- `,` prints a character exactly.

If the expected output is a clean integer with no trailing spaces, write or
generate a digit printer using `,`. Do not rely on `.` unless the harness
accepts the trailing space for that problem.

### 4. Prefer compiler-friendly algorithms.

Strong runs chose algorithms that map cleanly to Befunge storage and routing:

- For streaming text transforms, keep only a few variables: previous char,
  current char, flags, counters.
- For line-based tasks, build reusable line readers that handle newline and EOF.
- For array/string tasks, use explicit storage rows and simple loops.
- For hard dynamic indexing, sometimes a simpler algorithm is more reliable
  than a clever low-level pointer trick.
- If a merge or search problem becomes routing-heavy, consider buffering and
  using a simpler generated loop structure.

### 5. Test the generated program, not just the Python logic.

Python simulations are useful, but the submitted artifact is `.b98`. Always run
the generated Befunge program through:

```bash
python harness.py run solution.b98 --input "..."
```

Test:

- Empty lines and EOF-terminated input.
- Single values and multi-value lines.
- Negative numbers and zero.
- Duplicates.
- Long strings.
- Boundary formatting: no extra spaces, no missing newline assumptions.

### 6. Debug at the generator level.

If a local run loops or prints junk:

- Check whether the instruction pointer can fall into data/storage rows.
- Check branch direction: `_` and `|` consume a value and route differently on
  zero vs nonzero.
- Check stack order: arithmetic pops `b` then `a`, computes `a op b`.
- Check `.` vs `,` formatting.
- Check whether your grid placement overwrote earlier code.

## Required Startup Ritual Per Problem

1. Decide whether the task is tiny enough for direct Befunge or needs a
   generator.
2. For generator tasks, start from `reference_lib/`.
3. Choose a layout: 2D grid generator or 1D label assembler.
4. Reserve code rows and storage rows before writing logic.
5. Run the generated `.b98` through the local harness on a diverse test set.
6. If the run loops or formats output incorrectly, debug the generator/layout
   first rather than patching random cells by hand.

## Reference Files You May Use

- `reference_lib/opus_simulate.py`
  - local Befunge-98 simulator: pointer-machine over a 2D grid, stack ops,
    string mode, basic I/O. Use it to verify candidate Befunge programs
    locally before submitting.

The reference library is intentionally library-only: no per-problem
generators are provided. You build the problem-specific logic on top of
this simulator.

## Sanitized Strategy Examples

### Example A: Numeric problems.

For simple arithmetic, `&` may read integers directly. But for exact formatting,
generate a character-based integer printer. Test positive, negative, zero, and
multi-digit outputs.

### Example B: Streaming string transform.

For tasks like removing consecutive duplicates or counting spaces, avoid
buffering the entire input unless necessary. Track current char, previous char,
and flags. Test empty input, one char, all same chars, alternating chars, and
strings containing spaces.

### Example C: Rotation / substring-style tasks.

Use high-level algorithm selection before generating Befunge. For string
rotation, a reliable strategy is to check whether one string is a substring of
the other string doubled. Generate the storage/search logic carefully and test
equal strings, empty cases, non-rotations, and repeated-character strings.

## Start

If this is a fresh session, run:

```bash
python harness.py init --language befunge98 --budget inf
python harness.py fetch
```

If already initialized, do not reinitialize. Start with:

```bash
python harness.py fetch
```
