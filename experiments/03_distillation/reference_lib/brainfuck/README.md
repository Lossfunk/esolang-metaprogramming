# Brainfuck Reference Library (distillation `+library` condition)

This directory holds the *strategy library* used in the
`+library` distillation condition (Section 3.3 of the paper).

It is intentionally **library only** — general strategy scaffolds and
helper code, no per-problem generators or finished solutions. The
experimental contrast is whether the agent can *build* a working
generator from reusable scaffolding, not whether it can copy a finished
solution.

## What's here

| File | Role |
|---|---|
| `meta_bflib.py` | Generic BF code-generation library: `BF` builder class, BCD-arithmetic helpers, cell-allocator pattern, decimal print primitives. |
| `gpt5_xhigh_bf_codegen.py` | Stable cell-layout / builder pattern with `BFBuilder` dataclass and `alloc` / `clear` / `move_to` primitives. |
| `opus_learning_notes.md` | Strategy notes Opus wrote during its own session (state-tracking discipline, common pitfalls, cell-layout discipline). |

## Allowed use (this is the `+library` condition)

- Read these files, copy code from them, rename them, edit heavily.
- Build your own generator on top of them.
- The final submitted Brainfuck program must still pass the hidden tests
  via `python harness.py submit <id> <file>`.

## Not allowed

- Reading sibling experiment folders, transcripts, or any private tests.
- Copying solved benchmark programs from any source.

## Recommended reading order

1. `opus_learning_notes.md`
2. `meta_bflib.py`
3. `gpt5_xhigh_bf_codegen.py`

The point is to reuse the **structure** so you do not start from raw
Brainfuck on every problem.
