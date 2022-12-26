global debug_mode
debug_mode = False

from functools import cmp_to_key
def debug(*s):
    if debug_mode:
        print(s)

def read_file(filename = 'in2.txt'):
    with open(filename) as f:
        return [eval(line.strip()) for line in f.readlines() if line.strip()]

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))

def parse_lines(lines):
    return lines

def compare(a, b):
    if type(a) == int and type(b) == int:
        debug("int, int")
        return (a > b) - (a < b)
    elif type(a) == list and type(b) == list:
        debug("list, list")
        for res in map(compare, a, b):
            if res:
                return res
        return compare(len(a), len(b))
    else:
        if type(a) == int:
            return compare([a], b)
        elif type(b) == int:
            return compare(a, [b])

def solve(parsed_lines):
    ans = 0
    codes = parsed_lines
    s = sorted(codes, key=cmp_to_key(compare))
    return (s.index([[2]]) + 1) * (s.index([[6]])+1)

if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    ans = solve(parsed_lines)
    print(ans)
    # for line in ans:
    #     print(line)