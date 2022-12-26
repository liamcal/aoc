def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return [line.split() for line in lines]


def is_sample_cycle(n):
    return (n - 20) % 40 == 0


class CRT():
    def __init__(self):
        self.cycle = 0
        self.register = 1

    def noop(self):
        return self.increment_cycle()

    def add(self, n):
        increase = self.increment_cycle(times=2)
        self.register += n
        return increase

    def increment_cycle(self, times=1):
        increase = 0
        for _ in range(times):
            self.cycle += 1
            if (is_sample_cycle(self.cycle)):
                increase += self.cycle * self.register
        return increase


def solve(parsed_lines):
    screen = CRT()
    ans = 0
    for command in parsed_lines:
        instruction = command[0]
        if instruction == 'noop':
            ans += screen.noop()
        if instruction == 'addx':
            value = int(command[1])
            ans += screen.add(value)
    return (ans, screen.cycle, screen.register)


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
