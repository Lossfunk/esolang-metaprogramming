#!/usr/bin/env python3
"""Helpers for generating Brainfuck with a stable cell layout."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


BF_OPS = set("><+-.,[]")


BodyFn = Callable[["BFBuilder"], None]


@dataclass
class BFBuilder:
    pointer: int = 0
    cell_count: int = 0
    code: list[str] = field(default_factory=list)

    def alloc(self, size: int = 1) -> int:
        start = self.cell_count
        self.cell_count += size
        return start

    def emit(self, chunk: str) -> None:
        self.code.append(chunk)

    def move_to(self, cell: int) -> None:
        delta = cell - self.pointer
        if delta > 0:
            self.emit(">" * delta)
        elif delta < 0:
            self.emit("<" * (-delta))
        self.pointer = cell

    def clear(self, cell: int) -> None:
        self.move_to(cell)
        self.emit("[-]")

    def clear_many(self, cells: list[int]) -> None:
        for cell in cells:
            self.clear(cell)

    def add_const(self, cell: int, delta: int) -> None:
        self.move_to(cell)
        if delta > 0:
            self.emit("+" * delta)
        elif delta < 0:
            self.emit("-" * (-delta))

    def set_const(self, cell: int, value: int) -> None:
        self.clear(cell)
        self.add_const(cell, value % 256)

    def read_byte(self, cell: int) -> None:
        self.move_to(cell)
        self.emit(",")

    def write_byte(self, cell: int) -> None:
        self.move_to(cell)
        self.emit(".")

    def path(self, src: int, dst: int) -> str:
        if dst > src:
            return ">" * (dst - src)
        return "<" * (src - dst)

    def move_value(self, src: int, dst: int) -> None:
        if src == dst:
            return
        self.move_to(src)
        forward = self.path(src, dst)
        back = self.path(dst, src)
        self.emit(f"[{forward}+{back}-]")
        self.pointer = src

    def add_scaled(self, src: int, dst: int, delta: int) -> None:
        if delta == 0 or src == dst:
            return
        self.move_to(src)
        forward = self.path(src, dst)
        back = self.path(dst, src)
        op = "+" if delta > 0 else "-"
        self.emit(f"[{forward}{op * abs(delta)}{back}-]")
        self.pointer = src

    def copy_value(self, src: int, dst: int, tmp: int) -> None:
        if len({src, dst, tmp}) != 3:
            raise ValueError("copy_value requires distinct src, dst, and tmp cells")
        self.clear(dst)
        self.clear(tmp)
        self.move_to(src)
        to_dst = self.path(src, dst)
        back_dst = self.path(dst, src)
        to_tmp = self.path(src, tmp)
        back_tmp = self.path(tmp, src)
        self.emit(f"[{to_dst}+{back_dst}{to_tmp}+{back_tmp}-]")
        self.pointer = src
        self.move_value(tmp, src)

    def add_copy(self, src: int, dst: int, tmp: int) -> None:
        if len({src, dst, tmp}) != 3:
            raise ValueError("add_copy requires distinct src, dst, and tmp cells")
        self.clear(tmp)
        self.move_to(src)
        to_dst = self.path(src, dst)
        back_dst = self.path(dst, src)
        to_tmp = self.path(src, tmp)
        back_tmp = self.path(tmp, src)
        self.emit(f"[{to_dst}+{back_dst}{to_tmp}+{back_tmp}-]")
        self.pointer = src
        self.move_value(tmp, src)

    def sub_from(self, src: int, dst: int) -> None:
        if src == dst:
            raise ValueError("sub_from requires distinct src and dst cells")
        self.move_to(src)
        forward = self.path(src, dst)
        back = self.path(dst, src)
        self.emit(f"[{forward}-{back}-]")
        self.pointer = src

    def while_nonzero(self, cell: int, body: BodyFn) -> None:
        self.move_to(cell)
        self.emit("[")
        body(self)
        self.move_to(cell)
        self.emit("]")
        self.pointer = cell

    def if_nonzero_consume(self, cell: int, body: BodyFn) -> None:
        self.move_to(cell)
        self.emit("[[-]")
        body(self)
        self.move_to(cell)
        self.emit("]")
        self.pointer = cell

    def if_nonzero_keep(self, cell: int, copy_cell: int, restore_cell: int, body: BodyFn) -> None:
        self.copy_value(cell, copy_cell, restore_cell)
        self.if_nonzero_consume(copy_cell, body)

    def if_zero_keep(
        self,
        cell: int,
        copy_cell: int,
        restore_cell: int,
        flag_cell: int,
        body: BodyFn,
    ) -> None:
        self.set_const(flag_cell, 1)
        self.copy_value(cell, copy_cell, restore_cell)

        def clear_flag(builder: BFBuilder) -> None:
            builder.clear(flag_cell)

        self.if_nonzero_consume(copy_cell, clear_flag)
        self.if_nonzero_consume(flag_cell, body)

    def program(self) -> str:
        return "note generated\n" + "".join(self.code) + "\n"


def bf_only(source: str) -> str:
    return "".join(ch for ch in source if ch in BF_OPS)
