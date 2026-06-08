"""Shakespeare Programming Language interpreter wrapping shakespearelang."""

from __future__ import annotations

import io
import sys
from typing import Optional

from esolang_common import EsolangError


class ShakespeareInterpreter:
    LANGUAGE = "Shakespeare"

    def __init__(self, max_steps: int = 10_000_000) -> None:
        self.max_steps = max_steps

    def run(self, program: str, input_data: str = "") -> str:
        try:
            from shakespearelang import Shakespeare
        except ImportError:
            raise EsolangError(
                self.LANGUAGE,
                "EnvironmentError",
                "shakespearelang package not installed. Run: pip install shakespearelang",
            )

        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = io.StringIO(input_data)
        sys.stdout = captured = io.StringIO()
        try:
            s = Shakespeare(program, input_style="basic", output_style="basic")
            step_count = 0
            while not s.play_over():
                s.step_forward()
                step_count += 1
                if step_count >= self.max_steps:
                    raise EsolangError(
                        self.LANGUAGE,
                        "StepLimitExceeded",
                        f"Exceeded {self.max_steps} steps",
                    )
            return captured.getvalue()
        except EsolangError:
            raise
        except Exception as e:
            err_type = type(e).__name__
            if "parse" in err_type.lower() or "Parse" in str(type(e)):
                raise EsolangError(self.LANGUAGE, "ParseError", str(e))
            raise EsolangError(self.LANGUAGE, "RuntimeError", str(e))
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
