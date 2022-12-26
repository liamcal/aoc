SNAFU_BASE = 5
SNAFU_MAX_DIGIT = 2
SNAFU_NUM_LOOKUP = {'=': -2, '-': -1}
NUM_SNAFU_LOOKUP = {v: k for k, v in SNAFU_NUM_LOOKUP.items()}


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def num_to_snafu(n):
    ans_digits = []
    based = number_to_base(n, 5)
    carry = 0
    for digit in reversed(based):
        if carry:
            digit += carry
            carry = 0

        if digit >= SNAFU_BASE:
            digit -= SNAFU_BASE
            carry = 1

        if digit > SNAFU_MAX_DIGIT:
            excess = digit - SNAFU_BASE
            snafu_digit = NUM_SNAFU_LOOKUP[excess]
            carry = 1
        else:
            snafu_digit = digit
        ans_digits.append(str(snafu_digit))
    return ''.join(reversed(ans_digits))


def snafu_to_num(snafu):
    total = 0
    for power, digit in enumerate(reversed(snafu)):
        if digit in SNAFU_NUM_LOOKUP:
            total += SNAFU_NUM_LOOKUP[digit] * (SNAFU_BASE ** power)
        else:
            total += int(digit) * (SNAFU_BASE ** power)
    return total


def solve(lines):
    total = sum(snafu_to_num(snafu) for snafu in lines)
    print(total)
    return num_to_snafu(total)


if __name__ == '__main__':
    lines = read_file()
    print(solve(lines))
