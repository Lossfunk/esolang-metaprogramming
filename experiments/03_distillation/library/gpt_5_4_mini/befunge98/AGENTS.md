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

---

> **Start solving now.** The session is initialized. Begin by fetching your first problem:
> ```
> python harness.py fetch
> ```
> Work through all 80 problems sequentially. For each problem: read the description, generate your own test cases, use `run` to test, then `submit` when confident. Do NOT skip without attempting — see skip policy below.

# EsoLang-Bench: Befunge-98

You are solving 80 befunge-98 programming problems sequentially.
Problems span 4 difficulty tiers: E01-E20 (easy), M01-M20 (medium), H01-H20 (hard), X01-X20 (extra-hard).

Each problem has 6 hidden test cases you cannot see. No test cases are provided -- generate your own test inputs from the problem descriptions.

## Harness Commands

```bash
python harness.py fetch                          # Get next problem
python harness.py run <code_file> --input "..."  # Test with custom input (unlimited)
python harness.py submit <problem_id> <file>     # Hidden evaluation (max 3 per problem)
python harness.py status                         # Progress dashboard
python harness.py skip                           # Skip ONLY after attempting (see policy)
```

## Rules

- Solve problems in order. `fetch` advances to the next.
- Maximum 3 submissions per problem. Use `run` (unlimited) to test first.
- `submit` returns PASS/WRONG ANSWER/RUNTIME ERROR per hidden test -- no inputs or expected outputs shown.
- Problem is solved only if 6/6 hidden tests pass.
- Do not read private test files, reverse-engineer the harness, or hardcode outputs.

## CRITICAL: No Skipping — Use All 3 Submissions

- You MUST work on every problem until you either score 6/6 OR use all 3 submissions. Do NOT move to the next problem with unused submissions remaining.
- You CANNOT revisit problems later — once you move on, the problem is gone forever. Every unused submission is wasted.
- There is NO time limit. You have UNLIMITED time and UNLIMITED test runs (`run` command). The ONLY limit is 3 submissions per problem.
- For each problem: read the description, write a genuine solution, test it thoroughly with `run` using multiple inputs until it produces correct output, THEN submit.
- Do NOT submit untested code. Do NOT submit placeholder or stub solutions. Every submission must be a genuine, tested attempt.
- If a submission returns WRONG ANSWER or RUNTIME ERROR: analyze the failure, try a completely different approach, test it, then use your next submission.
- Even if a problem seems extremely difficult, you must use all 3 submissions with genuinely different approaches before moving on. A partial score (1-5/6) is far better than 0/6.
- Do NOT call `fetch` or `skip` to move to the next problem while you still have submissions remaining on the current one.


## Scoring

- Per problem: tests passed / 6
- Overall: problems solved / 80 and total tests passed / 480

## Befunge-98 Language Reference

### Program Structure

2D grid. Instruction pointer starts at (0,0) moving right. Wraps at edges. Ends at `@`.

### Instructions

**Stack:** `0-9` push digit; `a-f` push 10-15; `"` toggle string mode; `:` dup; `\` swap; `$` pop; `n` clear stack
**Arithmetic:** `+` `-` `*` `/` `%` (pop b, pop a, push a op b)
**Comparison:** `!` (NOT); `` ` `` (greater-than)
**Direction:** `>` `<` `^` `v` `?`(random) `[`(turn left) `]`(turn right) `r`(reverse) `#`(skip next) `j`(jump n)
**Branch:** `_` (right if 0, left if nonzero); `|` (down if 0, up if nonzero)
**I/O:** `.` print int+space; `,` print char; `&` read int; `~` read char (-1 at EOF)
**Grid:** `g` get; `p` put; `s` store next; `'` fetch next
**Flow:** `@` end; `q` quit; `;` comment toggle; space=nop

### Essential Patterns

- **Print string:** `"!dlroW olleH">:#,_@` (push reversed, loop print)
- **Print loop:** `>:#,_@` (dup, skip print if 0, print char, repeat)
- **Read int:** `&` (built-in)
- **Conditional:** `!#v_` (branch on value)

### Common Pitfalls

- **`.` trailing space**: `.` outputs number + space. For clean output, convert to digit chars and use `,`.
- **Stack order**: `52-` = 5-2=3, not 2-5.
- **String mode**: `"abc"` pushes a,b,c in order; they pop as c,b,a.
- **Missing `@`**: IP wraps and re-executes, hitting step limit.
- **`~` returns -1 at EOF**, not 0.
