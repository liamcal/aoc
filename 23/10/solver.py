import matplotlib.path as mpltPath


def parse(raw_data):
    return [list(line.strip()) for line in raw_data.split('\n')]


# (y, x)
# top left is 0, 0
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def get_next_dir(tile, dir):
    if tile == '-':
        if dir == RIGHT:
            return RIGHT
        elif dir == LEFT:
            return LEFT
    elif tile == '|':
        if dir == DOWN:
            return DOWN
        elif dir == UP:
            return UP
    elif tile == 'L':
        if dir == LEFT:
            return UP
        elif dir == DOWN:
            return RIGHT
    elif tile == 'J':
        if dir == RIGHT:
            return UP
        elif dir == DOWN:
            return LEFT
    elif tile == '7':
        if dir == RIGHT:
            return DOWN
        elif dir == UP:
            return LEFT
    elif tile == 'F':
        if dir == LEFT:
            return DOWN
        elif dir == UP:
            return RIGHT


def find_start(grid):
    for y, line in enumerate(grid):
        for x, pipe in enumerate(line):
            if pipe == 'S':
                return y, x


def find_starting_moves(grid, start_pos):
    y, x = start_pos
    moves = []
    if grid[y][x + 1] in ('-', '7', 'J'):
        moves.append(RIGHT)
    if grid[y][x - 1] in ('-', 'F', 'L'):
        moves.append(LEFT)
    if grid[y - 1][x] in ('|', '7', 'F'):
        moves.append(UP)
    if grid[y + 1][x] in ('|', 'J', 'L'):
        moves.append(DOWN)
    return moves


def get_path(grid):
    start_pos = find_start(grid)
    path = [start_pos]
    current_move = find_starting_moves(grid, start_pos)[0]
    current_pos = start_pos
    while True:
        next_pos = (current_pos[0] + current_move[0],
                    current_pos[1] + current_move[1])
        if next_pos == start_pos:
            break
        path.append(next_pos)
        next_tile = grid[next_pos[0]][next_pos[1]]
        next_move = get_next_dir(next_tile, current_move)
        current_pos, current_move = next_pos, next_move
    return path


def solve1(data):
    path = get_path(data)
    return len(path) // 2


def solve2(data):
    path = get_path(data)
    s_path = set(path)
    plt_path = mpltPath.Path(path)
    todo = [(y, x) for y in range(len(data))
            for x in range(len(data[0])) if (y, x) not in s_path]
    return sum(plt_path.contains_points(todo))


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
