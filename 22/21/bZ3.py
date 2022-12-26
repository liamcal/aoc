from z3 import Solver, Real

def read_file(filename='in2.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    s = Solver()
    vars = {'humn': Real('humn')}
    todo = []
    root = None
    for line in lines:
        monkey, value = line.split(": ")
        vars[monkey] = Real(monkey)
        if value.isdigit():
            s.add(vars[monkey] == int(value))
        else:
            if monkey == 'root':
                a, _, b = value.split()
                root = (a, b)
            else:
                todo.append((monkey, value.split()))
    return vars, todo, root, s 


def solve(data):
    vars, todo, root, s = data

    s.add(vars['root'] == vars[root[0]])
    s.add(vars['root'] == vars[root[1]])

    for monkey, procedure in todo:
        a, operator, b = procedure
        if operator == '+':
            s.add(vars[monkey] == vars[a] + vars[b])
        elif operator == '-':
            s.add(vars[monkey] == vars[a] - vars[b])
        elif operator == '*':
            s.add(vars[monkey] == vars[a] * vars[b])
        elif operator == '/':
            s.add(vars[monkey] == vars[a] / vars[b])
  
    # print('solver', s)
    s.check()
    m = s.model()
    return m[vars['humn']]


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
