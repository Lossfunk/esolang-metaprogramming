#!/usr/bin/env python3
"""Minimal Befunge-98 simulator to verify programs locally."""
import sys

def run(code, input_data, max_steps=1_000_000, trace=False):
    lines = code.split('\n')
    width = max(len(l) for l in lines)
    height = len(lines)
    grid = [[ord(' ')] * width for _ in range(height)]
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            grid[y][x] = ord(ch)

    def get(x, y):
        return grid[y % height][x % width]

    x, y = 0, 0
    dx, dy = 1, 0
    stack = []
    output = []
    string_mode = False
    input_pos = 0
    steps = 0

    def pop():
        return stack.pop() if stack else 0

    while steps < max_steps:
        steps += 1
        c = get(x, y)
        ch = chr(c)
        if trace:
            print(f"step {steps}: ({x},{y}) ch={ch!r} stack={stack} dir=({dx},{dy})")

        if string_mode:
            if ch == '"':
                string_mode = False
            else:
                stack.append(c)
        else:
            if ch == '"':
                string_mode = True
            elif ch == ' ':
                pass
            elif ch.isdigit():
                stack.append(int(ch))
            elif ch in 'abcdef':
                stack.append(10 + ord(ch) - ord('a'))
            elif ch == '+':
                b = pop(); a = pop(); stack.append(a + b)
            elif ch == '-':
                b = pop(); a = pop(); stack.append(a - b)
            elif ch == '*':
                b = pop(); a = pop(); stack.append(a * b)
            elif ch == '/':
                b = pop(); a = pop()
                if b == 0:
                    stack.append(0)
                else:
                    # Python's // does floor; Befunge-98 uses truncation toward zero
                    q = abs(a) // abs(b)
                    if (a < 0) ^ (b < 0):
                        q = -q
                    stack.append(q)
            elif ch == '%':
                b = pop(); a = pop()
                if b == 0:
                    stack.append(0)
                else:
                    q = abs(a) // abs(b)
                    if (a < 0) ^ (b < 0):
                        q = -q
                    stack.append(a - q * b)
            elif ch == '!':
                a = pop(); stack.append(1 if a == 0 else 0)
            elif ch == '`':
                b = pop(); a = pop(); stack.append(1 if a > b else 0)
            elif ch == ':':
                a = stack[-1] if stack else 0
                stack.append(a)
            elif ch == '\\':
                if len(stack) >= 2:
                    stack[-1], stack[-2] = stack[-2], stack[-1]
                elif len(stack) == 1:
                    stack.insert(0, 0)
                else:
                    stack.append(0); stack.append(0)
            elif ch == '$':
                pop()
            elif ch == '>':
                dx, dy = 1, 0
            elif ch == '<':
                dx, dy = -1, 0
            elif ch == '^':
                dx, dy = 0, -1
            elif ch == 'v':
                dx, dy = 0, 1
            elif ch == '?':
                import random
                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            elif ch == '[':
                dx, dy = dy, -dx
            elif ch == ']':
                dx, dy = -dy, dx
            elif ch == 'r':
                dx, dy = -dx, -dy
            elif ch == '#':
                x = (x + dx) % width
                y = (y + dy) % height
            elif ch == '_':
                a = pop()
                dx, dy = (1, 0) if a == 0 else (-1, 0)
            elif ch == '|':
                a = pop()
                dx, dy = (0, 1) if a == 0 else (0, -1)
            elif ch == '.':
                output.append(str(pop()) + ' ')
            elif ch == ',':
                output.append(chr(pop() % 256))
            elif ch == '&':
                # skip whitespace, read integer
                sign = 1
                while input_pos < len(input_data) and input_data[input_pos] in ' \t\n':
                    input_pos += 1
                if input_pos < len(input_data) and input_data[input_pos] == '-':
                    sign = -1; input_pos += 1
                n = 0
                has_digit = False
                while input_pos < len(input_data) and input_data[input_pos].isdigit():
                    n = n * 10 + int(input_data[input_pos])
                    input_pos += 1
                    has_digit = True
                stack.append(sign * n if has_digit else 0)
            elif ch == '~':
                if input_pos < len(input_data):
                    stack.append(ord(input_data[input_pos]))
                    input_pos += 1
                else:
                    stack.append(-1)
            elif ch == '@' or ch == 'q':
                return ''.join(output)
            elif ch == 'n':
                stack.clear()
            elif ch == "'":
                # Fetch: push ASCII of next cell, advance past it
                nx = (x + dx) % width
                ny = (y + dy) % height
                stack.append(grid[ny][nx])
                x, y = nx, ny
            elif ch == 'g':
                y2 = pop(); x2 = pop()
                if 0 <= x2 < width and 0 <= y2 < height:
                    stack.append(grid[y2][x2])
                else:
                    stack.append(0)
            elif ch == 'p':
                y2 = pop(); x2 = pop(); v2 = pop()
                # Expand grid if needed
                while y2 >= len(grid):
                    grid.append([ord(' ')] * width)
                    height = len(grid)
                if x2 >= width:
                    for row in grid:
                        row.extend([ord(' ')] * (x2 + 1 - width))
                    width = x2 + 1
                if 0 <= x2 < width and 0 <= y2 < height:
                    grid[y2][x2] = v2 & 0xFF
            elif ch == ';':
                # comment: skip until next ;
                while True:
                    x = (x + dx) % width
                    y = (y + dy) % height
                    if get(x, y) == ord(';'):
                        break
            # else: ignore unknown

        x = (x + dx) % width
        y = (y + dy) % height

    return ''.join(output) + '[STEP LIMIT]'

if __name__ == '__main__':
    code_file = sys.argv[1]
    input_data = sys.argv[2] if len(sys.argv) > 2 else ''
    code = open(code_file).read()
    print(repr(run(code, input_data)))
