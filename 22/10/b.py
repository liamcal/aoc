def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return [line.split() for line in lines]


class CRT():
    def __init__(self):
        self.width = 40
        self.height = 6
        self.cycle = 0
        self.register = 1
        self.screen = [['.' for i in range(self.width)]
                       for j in range(self.height)]

    def noop(self):
        self.increment_cycle()

    def add(self, n):
        self.increment_cycle(times=2)
        self.register += n

    def draw_pixel(self):
        y, x = divmod(self.cycle, self.width)
        if x >= self.register - 1 and x <= self.register + 1:
            self.screen[y][x] = "#"

    def increment_cycle(self, times=1):
        for _ in range(times):
            self.draw_pixel()
            self.cycle += 1


def solve(parsed_lines):
    crt = CRT()
    for command in parsed_lines:
        instruction = command[0]
        if instruction == 'noop':
            crt.noop()
        if instruction == 'addx':
            value = int(command[1])
            crt.add(value)

    return crt.screen


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    ans = solve(parsed_lines)
    for line in ans:
        print(''.join(line))
