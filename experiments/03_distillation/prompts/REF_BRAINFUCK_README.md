# Brainfuck Reference Library

These files are intentionally provided as local scaffolds for the
prompt-distillation condition.

Allowed use:

- Read them.
- Copy code from them.
- Rename them.
- Edit them heavily.
- Delete parts you do not need.
- Build your own generator/library on top of them.

Not allowed:

- Reading any parent/sibling experiment folders beyond this local workspace.
- Using private tests or hidden solution artifacts.

Recommended reading order:

1. `opus_learning_notes.md`
2. `meta_bflib.py`
3. `gpt5_xhigh_bf_codegen.py`
4. Build problem-specific logic on top.

Suggested file roles:

- `opus_learning_notes.md`: reusable strategy notes from an Opus 4.6 run
  (state-tracking discipline, common pitfalls, cell-layout discipline).
- `meta_bflib.py`: generic BCD/codegen helper library — `BF` builder class,
  cell allocator, decimal print primitives, BCD arithmetic helpers.
- `gpt5_xhigh_bf_codegen.py`: stable cell-layout / builder pattern with
  `BFBuilder` dataclass and `alloc` / `clear` / `move_to` primitives.

The library is intentionally library-only. No per-problem generators are
shipped: the experimental contrast is whether the agent can build working
generators on top of these scaffolds, not whether it can copy finished
solutions.

