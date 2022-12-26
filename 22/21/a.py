def read_file(filename='inCheck.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    done_monkeys = {}
    todo = []
    for line in lines:
        monkey, value = line.split(": ")
        if value.isdigit():
            done_monkeys[monkey] = int(value)
        else:
            todo.append((monkey, value.split()))
    return done_monkeys, todo


def solve(data):
    done_monkeys, todo = data
    while todo:
        current = todo.pop(0)
        monkey, operation = current
        a, operator, b = operation
        if a in done_monkeys and b in done_monkeys:
            a_val, b_val = done_monkeys[a], done_monkeys[b]
            if operator == '+':
                res = a_val + b_val
            elif operator == '-':
                res = a_val - b_val
            elif operator == '*':
                res = a_val * b_val
            elif operator == '/':
                res = a_val // b_val
            done_monkeys[monkey] = res
        else:
            todo.append(current)
    return done_monkeys['root'], done_monkeys['rnsd'], done_monkeys['vlzj'], done_monkeys['humn']


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
