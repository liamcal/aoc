def read_file(filename='in2.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    done_monkeys = {}
    todo = []
    root = None
    for line in lines:
        monkey, value = line.split(": ")
        if value.isdigit():
            done_monkeys[monkey] = int(value)
        else:
            if monkey == 'root':
                a, _, b = value.split()
                root = (a, b)
            else:
                todo.append((monkey, value.split()))
    return done_monkeys, todo, root


def solve(data):
    done_monkeys_og, todo_og, root, = data
    found = False
    i = 510000
    while not found:
        if i % 1000 == 0: 
            print("Up to", i)
        done_monkeys = done_monkeys_og | {'humn': i}
        todo = todo_og + []
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
                    res = a_val / b_val
                done_monkeys[monkey] = res
            else:
                todo.append(current)
        if done_monkeys[root[0]] == done_monkeys[root[1]]:
            print("FOUND", i, done_monkeys[root[0]])
            found = True
        else:
            i += 1
    return i


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
