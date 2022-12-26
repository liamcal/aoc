global debug_mode
debug_mode = False

def debug(*s):
    if debug_mode:
        print(s)

def read_file(filename = 'in.txt'):
    with open(filename) as f:
        return [eval(line.strip()) for line in f.readlines() if line.strip()]

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))

def parse_lines(lines):
    return list(chunks(lines, 2))

def compare(a, b):
    debug("comparing", a, b)
    debug("a_0:", type(a), a)
    debug("b_0:", type(b), b)
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
            debug("int, list")
            return compare([a], b)
        elif type(b) == int:
            debug("list, int")
            return compare(a, [b])

def solve(parsed_lines):
    ans = 0
    pairs = parsed_lines
    for i, pair in enumerate(pairs):
        a, b = pair
        print("Comparing")
        print(a)
        print(b)
        if compare(a, b) == -1:
            print("Correct")
            ans += i+1
        else:
            print("Incorrect")
        print()
    return ans

if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    ans = solve(parsed_lines)
    print(ans)