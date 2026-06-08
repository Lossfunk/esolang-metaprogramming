# Befunge-98 Reference Library

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

1. `opus_simulate.py` — local Befunge-98 simulator for verifying candidates.
2. Build problem-specific logic on top.

Suggested file roles:

- `opus_simulate.py`: local execution/debugging helper covering pointer
  routing, stack ops, string mode, and basic I/O.

The library is intentionally library-only. No per-problem generators are
shipped: the experimental contrast is whether the agent can build working
solutions on top of a reusable simulator, not whether it can copy finished
generators.

