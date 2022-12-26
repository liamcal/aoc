"""
TODO:
Build the grid on parse
Remove hardcoded values
Fix coord ordering

"""

global debug_mode
debug_mode = False


def debug(*s):
    if debug_mode:
        print(s)


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


class StraightLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.is_horizontal = self.y1 == self.y2
        self.is_vertical = self.x1 == self.x2
        if not self.is_horizontal and not self.is_vertical:
            raise ValueError(
                "Line must be vertical or horizontal", x1, y1, x2, y2)

    def is_on_line(self, x, y):
        if self.is_horizontal:
            return y == self.y1 and x >= min(self.x1, self.x2) and x <= max(self.x1, self.x2)
        else:
            return x == self.x1 and y >= min(self.y1, self.y2) and x <= max(self.y1, self.y2)

    def __repr__(self):
        return f'<Line: ({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})>'

    def get_coords(self):
        coords = []
        if self.is_vertical:
            for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1):
                coords.append((self.x1, y))
        else:
            for x in range(min(self.x1, self.x2), max(self.x1, self.x2) + 1):
                coords.append((x, self.y1))
        return coords


X_OFFSET = 471
Y_OFFSET = 0
WIDTH = 80
HEIGHT = 180


def parse_lines(lines):
    straightLines = []
    for line in lines:
        current_instruction_line = []
        current_coords = []
        instructions = line.split(' -> ')
        for instruction in instructions:
            x, y = map(int, instruction.split(','))
            x1 = x - X_OFFSET
            y1 = y - Y_OFFSET
            if x1 < 0 or y1 < 0:
                raise ValueError("Coord out of bounds", x, y, x1, y1)
            current_instruction_line.append((x1, y1))
        for i in range(len(current_instruction_line) - 1):
            x1, y1 = current_instruction_line[i]
            x2, y2 = current_instruction_line[i + 1]

            straightLines.append(StraightLine(x1, y1, x2, y2))
    return straightLines


def spawn_grain(grid, x, y):
    cur_x, cur_y = x, y
    y_max = len(grid)
    x_max = len(grid[0])
    while True:
        debug(cur_y, cur_x) 
        if cur_y + 1 >= y_max: 
            return 0
        debug(grid[cur_y + 1][cur_x - 1], grid[cur_y + 1][x], grid[cur_y + 1][cur_x + 1])
        if grid[cur_y + 1][cur_x] == '.':
            cur_y, cur_x = cur_y + 1, cur_x
        elif grid[cur_y + 1][cur_x - 1] == '.':
            cur_y, cur_x = cur_y + 1, cur_x - 1
        elif grid[cur_y + 1][cur_x + 1] == '.':
            cur_y, cur_x = cur_y + 1, cur_x + 1
        else:
            grid[cur_y][cur_x] = 'o'
            for line in grid:
                debug(''.join(line))
            debug()
            return 1


def solve(parsed_lines):
    straightLines = parsed_lines
    grid = [['.' for _ in range(WIDTH)] for __ in range(HEIGHT)]
    for line in straightLines:
        coords = line.get_coords()
        for x, y in coords:
            grid[y][x] = '#'

    xs, ys = 500 - X_OFFSET, 0 - Y_OFFSET
    grid[ys][xs] = '+'

    spawning = True
    count = 0
    while spawning:
        spawning = spawn_grain(grid, xs, ys)
        if spawning:
            count += 1
    return grid, count


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    grid, count = solve(parsed_lines)
    debug("###ANS###")
    print(count)
    for line in grid:
        print(''.join(line))

