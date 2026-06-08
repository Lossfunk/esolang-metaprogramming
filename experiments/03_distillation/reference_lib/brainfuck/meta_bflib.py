#!/usr/bin/env python3
"""BF code generation library with BCD arithmetic."""


class BF:
    def __init__(self):
        self.code = []
        self.ptr = 0

    def goto(self, pos):
        diff = pos - self.ptr
        if diff > 0: self.code.append('>' * diff)
        elif diff < 0: self.code.append('<' * (-diff))
        self.ptr = pos

    def raw(self, s):
        for ch in s:
            if ch == '>': self.ptr += 1
            elif ch == '<': self.ptr -= 1
        self.code.append(s)

    def inc(self, pos, val):
        self.goto(pos)
        if val > 0: self.code.append('+' * val)
        elif val < 0: self.code.append('-' * (-val))

    def zero(self, pos):
        self.goto(pos)
        self.code.append('[-]')

    def read(self, pos):
        self.goto(pos)
        self.code.append(',')

    def write(self, pos):
        self.goto(pos)
        self.code.append('.')

    def set_val(self, pos, val):
        self.zero(pos)
        if val > 0: self.inc(pos, val)

    def move_to(self, src, dst):
        """dst += src; src = 0"""
        self.goto(src)
        diff = dst - src
        if diff > 0:
            self.code.append('[-' + '>' * diff + '+' + '<' * diff + ']')
        elif diff < 0:
            self.code.append('[-' + '<' * (-diff) + '+' + '>' * (-diff) + ']')

    def move_to2(self, src, dst1, dst2):
        """dst1 += src; dst2 += src; src = 0"""
        self.goto(src)
        parts = []
        for dst in [dst1, dst2]:
            diff = dst - src
            if diff > 0: parts.append('>' * diff + '+' + '<' * diff)
            else: parts.append('<' * (-diff) + '+' + '>' * (-diff))
        self.code.append('[-' + ''.join(parts) + ']')

    def copy(self, src, dst, tmp):
        """dst = src (additive to dst). Uses tmp. Both dst and tmp should be 0."""
        self.move_to2(src, dst, tmp)
        self.move_to(tmp, src)

    def sub_from(self, src, dst):
        """dst -= src; src = 0"""
        self.goto(src)
        diff = dst - src
        if diff > 0:
            self.code.append('[-' + '>' * diff + '-' + '<' * diff + ']')
        elif diff < 0:
            self.code.append('[-' + '<' * (-diff) + '-' + '>' * (-diff) + ']')

    def result(self):
        return ''.join(self.code)


class CellAlloc:
    """Simple cell allocator."""
    def __init__(self, start=0):
        self.next = start

    def alloc(self, n=1):
        if n == 1:
            c = self.next
            self.next += 1
            return c
        else:
            cells = list(range(self.next, self.next + n))
            self.next += n
            return cells

    def alloc_bcd(self, ndigits):
        """Allocate cells for a BCD number: digits + sign."""
        digits = self.alloc(ndigits)
        sign = self.alloc()
        return digits, sign


def check_eq(bf, cell, value, flag, tmp):
    """flag = 1 if cell == value, else 0. cell preserved."""
    bf.zero(tmp)
    bf.zero(flag)
    bf.copy(cell, tmp, flag)  # tmp = cell
    if value > 0:
        bf.inc(tmp, -value)
    elif value < 0:
        bf.inc(tmp, -value)
    bf.set_val(flag, 1)
    bf.goto(tmp)
    bf.raw('[')
    bf.zero(flag)
    bf.zero(tmp)
    bf.goto(tmp)
    bf.raw(']')


def if_nonzero(bf, cell, body_fn, tmp):
    """Execute body_fn if cell != 0. cell is preserved. tmp must be 0."""
    bf.zero(tmp)
    bf.copy(cell, tmp, bf_tmp_scratch)  # Hmm, need another temp
    # Actually, let's use a simpler interface
    pass


def divmod10(bf, cell, quot, counter, flag, tmp1, tmp2):
    """cell = cell mod 10, quot = cell / 10. cell should be 0-99ish.
    quot must be 0. counter, flag, tmp1, tmp2 are temps (must be 0)."""
    bf.zero(quot)
    bf.set_val(counter, 10)

    bf.goto(cell)
    bf.raw('[')  # while cell > 0
    bf.inc(cell, -1)
    bf.inc(counter, -1)

    # if counter == 0: quot++, counter = 10
    bf.set_val(flag, 1)
    bf.zero(tmp1)
    bf.goto(counter)
    bf.raw('[')
    bf.zero(flag)
    bf.move_to(counter, tmp1)
    bf.goto(counter)
    bf.raw(']')
    bf.move_to(tmp1, counter)
    bf.goto(flag)
    bf.raw('[')
    bf.inc(quot, 1)
    bf.set_val(counter, 10)
    bf.zero(flag)
    bf.goto(flag)
    bf.raw(']')

    bf.goto(cell)
    bf.raw(']')

    # cell = 0, remainder = 10 - counter
    bf.set_val(cell, 10)
    bf.sub_from(counter, cell)


def read_bcd(bf, digits, sign, inp, temps, ndigits):
    """Read a signed integer into BCD cells (LSB first after shifting).
    digits: list of cell indices for digits.
    sign: cell for sign (0=pos, 1=neg).
    inp: cell for reading input.
    temps: list of at least 4 temp cells.
    """
    t0, t1, t2, t3 = temps[0], temps[1], temps[2], temps[3]

    for i in range(ndigits):
        bf.zero(digits[i])
    bf.zero(sign)

    bf.read(inp)

    # Check for minus
    check_eq(bf, inp, 45, t0, t1)
    bf.goto(t0)
    bf.raw('[')
    bf.set_val(sign, 1)
    bf.read(inp)
    bf.zero(t0)
    bf.goto(t0)
    bf.raw(']')

    # Read digits with shift-up technique (LSB ends in digits[0])
    bf.set_val(t0, 1)  # continue flag
    bf.goto(t0)
    bf.raw('[')

    # Check delimiters
    for delim in [0, 10, 32, 13]:
        check_eq(bf, inp, delim, t1, t2)
        bf.goto(t1)
        bf.raw('[')
        bf.zero(t0)
        bf.zero(t1)
        bf.goto(t1)
        bf.raw(']')

    # If still continuing, process digit
    bf.zero(t1)
    bf.zero(t2)
    bf.copy(t0, t1, t2)
    bf.goto(t1)
    bf.raw('[')

    # Shift digits up
    for i in range(ndigits - 2, -1, -1):
        bf.move_to(digits[i], digits[i + 1])

    # Store digit
    bf.zero(t2)
    bf.copy(inp, digits[0], t2)
    bf.inc(digits[0], -48)

    bf.read(inp)

    bf.zero(t1)
    bf.goto(t1)
    bf.raw(']')

    bf.goto(t0)
    bf.raw(']')


def negate_bcd(bf, digits, ndigits, temps):
    """10's complement negate in place. temps: at least 5 cells."""
    t0, t1, t2, t3, t4 = temps[0], temps[1], temps[2], temps[3], temps[4]

    # 9's complement
    for i in range(ndigits):
        bf.zero(t0)
        bf.move_to(digits[i], t0)
        bf.inc(digits[i], 9)
        bf.sub_from(t0, digits[i])

    # Add 1 with carry
    bf.inc(digits[0], 1)
    for i in range(ndigits):
        bf.zero(t0)
        divmod10(bf, digits[i], t0, t1, t2, t3, t4)
        if i < ndigits - 1:
            bf.move_to(t0, digits[i + 1])
        else:
            bf.zero(t0)


def conditional_negate_bcd(bf, digits, sign, ndigits, temps):
    """If sign != 0, negate digits. sign preserved."""
    t = temps
    bf.zero(t[0])
    bf.zero(t[1])
    bf.copy(sign, t[0], t[1])
    bf.goto(t[0])
    bf.raw('[')
    negate_bcd(bf, digits, ndigits, temps[1:6])
    bf.zero(t[0])
    bf.goto(t[0])
    bf.raw(']')


def add_bcd(bf, a_digits, b_digits, res_digits, ndigits, carry_cell, temps):
    """res = a + b in 10's complement BCD. LSB first.
    res_digits should have ndigits+1 cells (for overflow).
    carry_cell and temps (5 cells) must be 0."""
    t0, t1, t2, t3, t4 = temps[0], temps[1], temps[2], temps[3], temps[4]

    for i in range(ndigits + 1):
        bf.zero(res_digits[i])
    bf.zero(carry_cell)

    for i in range(ndigits):
        bf.move_to(a_digits[i], res_digits[i])
        bf.move_to(b_digits[i], res_digits[i])
        bf.move_to(carry_cell, res_digits[i])
        bf.zero(carry_cell)
        divmod10(bf, res_digits[i], carry_cell, t0, t1, t2, t3)

    bf.move_to(carry_cell, res_digits[ndigits])


def check_negative_bcd(bf, digits, ndigits, result_flag, temps):
    """Set result_flag = 1 if BCD number is negative (MSB >= 5). temps: 3 cells."""
    t0, t1, t2 = temps[0], temps[1], temps[2]
    bf.zero(result_flag)
    bf.zero(t0)
    bf.zero(t1)
    bf.copy(digits[ndigits - 1], t0, t1)
    bf.inc(t0, -5)
    # If t0 is 0-4 (original was 5-9): negative
    for v in range(5):
        check_eq(bf, t0, v, t1, t2)
        bf.goto(t1)
        bf.raw('[')
        bf.set_val(result_flag, 1)
        bf.zero(t1)
        bf.goto(t1)
        bf.raw(']')


def print_bcd(bf, digits, ndigits, sign_cell, temps, complement=True):
    """Print BCD number. If negative (sign_cell), print '-'.
    If complement=True, negate via 10's complement first (for addition results).
    If complement=False, digits are already absolute value (for multiplication).
    temps: at least 8 cells."""
    t = temps

    # If negative: print '-' and optionally negate
    bf.zero(t[0])
    bf.zero(t[1])
    bf.copy(sign_cell, t[0], t[1])
    bf.goto(t[0])
    bf.raw('[')
    bf.set_val(t[1], 45)
    bf.write(t[1])
    if complement:
        negate_bcd(bf, digits, ndigits, t[1:6])
    bf.zero(t[0])
    bf.goto(t[0])
    bf.raw(']')

    # Print digits, skip leading zeros
    bf.zero(t[0])  # "started" flag
    for i in range(ndigits - 1, 0, -1):
        bf.zero(t[1])
        bf.zero(t[2])
        bf.copy(digits[i], t[1], t[2])
        # Check if should print: t[0] > 0 or t[1] > 0
        bf.zero(t[2])
        bf.zero(t[3])
        bf.copy(t[0], t[2], t[3])
        bf.zero(t[3])
        bf.zero(t[4])
        bf.copy(t[1], t[3], t[4])
        bf.move_to(t[3], t[2])
        bf.goto(t[2])
        bf.raw('[')
        bf.zero(t[3])
        bf.zero(t[4])
        bf.copy(digits[i], t[3], t[4])
        bf.inc(t[3], 48)
        bf.write(t[3])
        bf.set_val(t[0], 1)
        bf.zero(t[2])
        bf.goto(t[2])
        bf.raw(']')

    # Always print ones
    bf.zero(t[1])
    bf.zero(t[2])
    bf.copy(digits[0], t[1], t[2])
    bf.inc(t[1], 48)
    bf.write(t[1])


def multiply_bcd(bf, a_digits, b_digits, res_digits, ndigits, res_ndigits, temps):
    """Multiply two BCD numbers (absolute values, no sign handling).
    a and b are ndigits each, result is res_ndigits.
    temps: at least 10 cells.
    a_digits and b_digits are destroyed."""
    t = temps

    # Clear result
    for i in range(res_ndigits):
        bf.zero(res_digits[i])

    # Schoolbook multiplication:
    # for j in range(ndigits):  (each digit of b)
    #   for i in range(ndigits):  (each digit of a)
    #     product_position = i + j
    #     res[product_position] += a[i] * b[j]
    #     carry propagation

    # For each digit b[j]:
    #   Multiply a by b[j] (single digit), add to result shifted by j.

    # Single digit multiply: a[i] * d
    # = add a[i] to accumulator d times.
    # Use: copy d to counter. Loop counter times: add a[i] to accumulator.

    for j in range(ndigits):
        # For each digit of b: add a * b[j] to result at offset j

        # Copy b_digits[j] to counter (t[0])
        bf.zero(t[0])
        bf.zero(t[1])
        bf.copy(b_digits[j], t[0], t[1])

        # Loop t[0] times: each iteration adds a to result[j..]
        bf.goto(t[0])
        bf.raw('[')
        bf.inc(t[0], -1)

        for i in range(ndigits):
            if i + j < res_ndigits:
                bf.zero(t[1])
                bf.zero(t[2])
                bf.copy(a_digits[i], t[1], t[2])
                bf.move_to(t[1], res_digits[i + j])

        bf.goto(t[0])
        bf.raw(']')

        # Propagate carries after each digit of b to prevent overflow
        for i in range(j, min(j + ndigits + 1, res_ndigits - 1)):
            bf.zero(t[0])
            divmod10(bf, res_digits[i], t[0], t[1], t[2], t[3], t[4])
            bf.move_to(t[0], res_digits[i + 1])

    # Final carry propagation for any remaining
    for i in range(res_ndigits - 1):
        bf.zero(t[0])
        divmod10(bf, res_digits[i], t[0], t[1], t[2], t[3], t[4])
        bf.move_to(t[0], res_digits[i + 1])

    bf.zero(t[0])
    divmod10(bf, res_digits[res_ndigits - 1], t[0], t[1], t[2], t[3], t[4])


def gen_add(ndigits=10):
    """Generate BF for summing two integers."""
    bf = BF()
    alloc = CellAlloc()

    n1, s1 = alloc.alloc_bcd(ndigits)
    alloc.alloc(1)  # padding
    n2, s2 = alloc.alloc_bcd(ndigits)
    alloc.alloc(1)
    res = alloc.alloc(ndigits + 1)
    rs = alloc.alloc()
    alloc.alloc(1)
    inp = alloc.alloc()
    temps = alloc.alloc(10)

    read_bcd(bf, n1, s1, inp, temps, ndigits)
    conditional_negate_bcd(bf, n1, s1, ndigits, temps)

    read_bcd(bf, n2, s2, inp, temps, ndigits)
    conditional_negate_bcd(bf, n2, s2, ndigits, temps)

    add_bcd(bf, n1, n2, res, ndigits, temps[0], temps[1:6])

    check_negative_bcd(bf, res, ndigits, rs, temps)

    print_bcd(bf, res, ndigits, rs, temps)

    return bf.result()


def gen_multiply(ndigits=6):
    """Generate BF for multiplying two integers."""
    bf = BF()
    alloc = CellAlloc()
    res_ndigits = ndigits * 2

    n1, s1 = alloc.alloc_bcd(ndigits)
    alloc.alloc(1)
    n2, s2 = alloc.alloc_bcd(ndigits)
    alloc.alloc(1)
    res = alloc.alloc(res_ndigits)
    rs = alloc.alloc()  # result sign
    alloc.alloc(1)
    inp = alloc.alloc()
    temps = alloc.alloc(10)

    # Read numbers
    read_bcd(bf, n1, s1, inp, temps, ndigits)
    read_bcd(bf, n2, s2, inp, temps, ndigits)

    # Result sign = sign1 XOR sign2
    # XOR: rs = s1 + s2; if rs == 2: rs = 0
    bf.zero(rs)
    bf.move_to(s1, rs)
    bf.move_to(s2, rs)
    # If rs == 2, set to 0
    check_eq(bf, rs, 2, temps[0], temps[1])
    bf.goto(temps[0])
    bf.raw('[')
    bf.zero(rs)
    bf.zero(temps[0])
    bf.goto(temps[0])
    bf.raw(']')

    # Multiply absolute values
    multiply_bcd(bf, n1, n2, res, ndigits, res_ndigits, temps)

    # Print with sign (absolute value, no complement)
    print_bcd(bf, res, res_ndigits, rs, temps, complement=False)

    return bf.result()


if __name__ == '__main__':
    import sys
    prob = sys.argv[1] if len(sys.argv) > 1 else ''
    if prob == 'E04':
        print(gen_add())
    elif prob == 'E05':
        print(gen_multiply())
    else:
        print(f"Unknown problem: {prob}")
