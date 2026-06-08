# EsoLang-Bench Prompt Distillation: Brainfuck

You are solving 80 programming problems in **Brainfuck** through a local
evaluation harness.

This workspace is the paper's **prompt-distillation** condition. You are given
high-level strategies distilled from stronger successful runs, but no solved
programs, no hidden tests, and no prior generated artifacts.

## Evaluation Policy

- Local interpreter calls are unbounded.
- Use `python harness.py run <file> --input "..."` freely before submission.
- Maximum hidden-test submissions: **1 per problem**.
- The single `submit` is blind and final for that problem.
- The final submitted file must be a valid `.bf` Brainfuck program.

## Harness Commands

```bash
python harness.py init --language brainfuck --budget inf
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
- `reference_lib/opus_learning_notes.md`
- `reference_lib/meta_bflib.py`
- `reference_lib/gpt5_xhigh_bf_codegen.py`

These are intentionally provided as local strategy scaffolds distilled from
stronger **Opus 4.6** and **GPT-5.4 xhigh** runs. They contain library-level
patterns only — no per-problem generators. You may read, copy, rename, edit,
and extend them.

### 1. Treat Python as a compiler, not a scratchpad.

For non-trivial problems, write Python that **generates Brainfuck**. The Python
script is your compiler: it should manage cell allocation, pointer movement,
copy/move/clear primitives, branching patterns, input parsing, and output
formatting.

Do not merely concatenate ad-hoc Brainfuck strings. Build a small local
generator library with:

- `alloc(name, count)` for stable cell layouts.
- `move_to(cell)`, `emit(code)`, `clear(cell)`, `set_const(cell, value)`.
- Non-destructive `copy(src, dst, tmp)`.
- Destructive `move(src, dst)`.
- Boolean helpers: `is_zero`, `is_nonzero`, `eq_const`.
- A safe `if_flag(flag, body)` pattern that consumes or clears branch flags.
- String output helpers that use one temporary cell and character deltas.

Operational rule:

- If the problem is more than a tiny fixed-string or single-character transform,
  default to writing or adapting a Python generator first.

### 2. Build reusable numeric I/O immediately.

Brainfuck failures usually come from ASCII numeric I/O, not the high-level
algorithm. When a problem says "integer", assume hidden tests may include:

- Multi-digit values.
- Zero.
- Negative values.
- Optional trailing newline or EOF termination.
- Whitespace separators.
- Outputs larger than 255.

Avoid raw byte arithmetic for general integer problems. Use decimal digit
arrays / BCD:

- Store each number as sign cell + array of decimal digits.
- Parse input one character at a time.
- Shift digit arrays when appending new digits.
- Add magnitudes digit-by-digit with carry.
- Subtract magnitudes with borrow using the `+10` trick to avoid unsigned
  underflow.
- Compare signed values by sign first, magnitude second.
- Print with leading-zero suppression and never print `-0`.

Operational rule:

- If the problem statement says "integer", "sum", "product", "average",
  "minimum", "maximum", "compare", "count", or "length", assume you should
  start from the decimal/BCD scaffolds unless you can clearly prove a smaller
  raw-byte solution is safe on hidden tests.

### 3. Keep reusable arithmetic primitives.

Strong runs reused the same components across many problems. Build and test:

- Signed decimal parse.
- Signed add/subtract.
- Magnitude compare.
- Min/max selection.
- Decimal output.
- Divmod by 10 for printing and carry propagation.
- Division by 2 via digit scan for average/halving tasks.
- Multiplication using grade-school digit loops when raw bytes are unsafe.

### 4. Use simple algorithms that are target-language-friendly.

Choose algorithms that are easiest to compile to Brainfuck, not necessarily
the most elegant in Python.

- Prefer streaming transforms for character problems.
- Prefer fixed stable cell layouts over dynamic pointer tricks.
- Prefer decimal arrays for arbitrary integer work.
- Prefer bounded arrays and explicit loops over clever self-modifying pointer
  layouts.
- If a complex algorithm needs dynamic indexing, consider a simpler
  alternative that is easier to generate and verify.

### 5. Verification discipline.

Before the one hidden submission, run many local tests. Include:

- Empty input where meaningful.
- Single-character and single-digit cases.
- Multi-digit values.
- Large values.
- Negative/positive mixtures.
- Zero and cancellation cases.
- Inputs with and without trailing newline.
- Boundary strings: all same chars, alternating chars, spaces, punctuation.

If local tests fail, fix the generator or library first. Do not patch random
Brainfuck by hand unless the program is tiny.

## Required Startup Ritual Per Problem

1. Decide whether this is a tiny direct Brainfuck task or a generator task.
2. For generator tasks, start from `reference_lib/` or your own local scaffold.
3. Write down the intended cell layout before adding algorithm logic.
4. For numeric tasks, choose decimal/BCD by default.
5. Run a diverse local test set before the single hidden submission.
6. If local tests expose a bug, fix the generator/library, regenerate, and test
   again before submitting.

## Reference Files You May Use

- `reference_lib/meta_bflib.py`
  - generic Brainfuck code-generation library: `BF` builder class,
    BCD-arithmetic helpers, cell-allocator pattern, decimal print primitives.
- `reference_lib/gpt5_xhigh_bf_codegen.py`
  - stable cell-layout / builder pattern with `BFBuilder` dataclass and
    `alloc` / `clear` / `move_to` primitives (distilled from a GPT-5.4 xhigh run).
- `reference_lib/opus_learning_notes.md`
  - reusable strategy notes from an Opus 4.6 Brainfuck run: state-tracking
    discipline, common pitfalls, cell-layout discipline.

The reference library is intentionally library-only: no per-problem
generators are provided. You build the problem-specific logic on top of
these scaffolds.

## Sanitized Strategy Examples

### Example A: Sum two integers.

Do not assume `3 4`-style single digits. Build signed decimal parsing and
BCD addition/subtraction. Test `2 3`, `99 1`, `9999 1`, `-5 8`, `5 -8`,
`-5 -8`, `0 0`, and cancellation cases like `-5 5`.

### Example B: String length / counters.

A byte counter may pass short public-style checks but fail on longer hidden
strings. Test lengths `0`, `1`, `9`, `10`, `11`, and larger. Print decimal
digits with leading-zero suppression.

### Example C: Comparisons.

For min/max/compare problems, do not compute `a-b` as a raw byte. Compare signs
first; for same sign compare magnitudes digit-by-digit. Remember that negative
ordering reverses magnitude order.

## Start

If this is a fresh session, run:

```bash
python harness.py init --language brainfuck --budget inf
python harness.py fetch
```

If already initialized, do not reinitialize. Start with:

```bash
python harness.py fetch
```
