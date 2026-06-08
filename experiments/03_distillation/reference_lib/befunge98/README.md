# Befunge-98 Reference Library (distillation `+library` condition)

This directory holds the *strategy library* used in the
`+library` distillation condition (Section 3.3 of the paper).

It is intentionally **library only** — a general Befunge-98 simulator
and helper code, no per-problem generators or finished solutions. The
experimental contrast is whether the agent can *build* a working
solution on top of a reusable simulator, not whether it can copy a
finished generator.

## What's here

| File | Role |
|---|---|
| `opus_simulate.py` | Minimal Befunge-98 simulator: pointer-machine over a 2D grid, stack ops, string mode, basic I/O. Used to verify candidate Befunge programs locally before submitting. |

## Recommended reading order

1. `opus_simulate.py` — local verification harness for candidate Befunge programs.
2. Build problem-specific logic on top.

## Allowed use

- Read this file, import it, edit it, extend it.
- Use the simulator to test Befunge programs you author or generate.
- The final submitted Befunge-98 program must pass the hidden tests via
  `python harness.py submit <id> <file>`.

## Not allowed

- Reading sibling experiment folders, transcripts, or any private tests.
- Copying solved benchmark programs from any source.
