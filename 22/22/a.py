import re


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.replace('\n', '') for line in f.readlines()]


def parse_map(lines):
    max_len = 0
    grid = []
    for line in lines:
        max_len = max(len(line), max_len)
        grid.append(list(line))

    for i, line in enumerate(grid):
        delta = max_len - len(line)
        grid[i] = line + [' ' for _ in range(delta)]
    return grid


def parse_instructions(instruction_line):
    instructions = re.split(r'([RL])', instruction_line[0])
    instructions = list(map(lambda x: x if x == 'L' or x ==
                        'R' else int(x), instructions))
    return instructions


EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

LEFT = -1
RIGHT = +1

moves = {
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    NORTH: (0, -1),
}


def turn(heading, turn):
    return (heading + turn) % 4


def move(heading, pos):
    step = moves[heading]
    return (pos[0] + step[0], pos[1] + step[1])


def wrap(grid, heading, pos):
    if heading == EAST:
        # find leftmost
        y = pos[1]
        for x in range(len(grid[0])):
            tile = grid[y][x]
            if tile == '.':
                return (x, y)
            elif tile == '#':
                return None  # can't wrap
        return None

    elif heading == SOUTH:
        # find topmost
        x = pos[0]
        for y in range(len(grid)):
            tile = grid[y][x]
            if tile == '.':
                return (x, y)
            elif tile == '#':
                return None  # can't wrap
        return None

    elif heading == WEST:
        # find rightmost
        y = pos[1]
        for x in reversed(range(len(grid[0]))):
            tile = grid[y][x]
            if tile == '.':
                return (x, y)
            elif tile == '#':
                return None  # can't wrap
        return None

    elif heading == NORTH:
        # find bottommost
        x = pos[0]
        for y in reversed(range(len(grid))):
            tile = grid[y][x]
            if tile == '.':
                return (x, y)
            elif tile == '#':
                return None  # can't wrap
        return None


def generate_password(heading, pos):
    return heading + (pos[1] + 1) * 1000 + (pos[0] + 1) * 4


def solve(grid, instructions):
    # print("GRID")
    # for line in grid:
    #     print(line)
    # print("INS")
    # print(instructions)
    height = len(grid)
    width = len(grid[0])
    first_row = grid[0]
    # print(first_row)
    for x, val in enumerate(first_row):
        if val == '.':
            break

    start_pos = (x, 0)
    current_pos = start_pos
    heading = EAST
    history = [(current_pos, heading)]

    while instructions:
        current_instructions = instructions.pop(0)
        print("Current", current_instructions, "remaining", len(instructions))
        if current_instructions == 'L':
            heading = turn(heading, LEFT)
        elif current_instructions == 'R':
            heading = turn(heading, RIGHT)
        else:
            distance = current_instructions
            travelled = 0
            while travelled < distance:
                next_pos = move(heading, current_pos)
                if (next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= width or next_pos[1] >= height):
                    wrap_pos = wrap(grid, heading, next_pos)
                    if wrap_pos is not None:
                        current_pos = wrap_pos
                else:
                    peek_next = grid[next_pos[1]][next_pos[0]]
                    if peek_next == '.':
                        current_pos = next_pos
                    elif peek_next == '#':
                        break
                    elif peek_next == ' ':
                        wrap_pos = wrap(grid, heading, next_pos)
                        if wrap_pos is not None:
                            current_pos = wrap_pos
                travelled += 1
        history.append((current_pos, heading))
    password = generate_password(heading, current_pos)
    return password


if __name__ == '__main__':
    map_contents = read_file('mapIn.txt')
    instructions_contents = read_file('instructionsIn.txt')
    parsed_lines = parse_map(map_contents)
    parsed_instructions = parse_instructions(instructions_contents)
    print(solve(parsed_lines, parsed_instructions))
