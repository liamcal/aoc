
def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    initial_blizzard = set()
    lines = [line[1:-1] for line in lines][1:-1]  # Trim the outside edges
    height = len(lines)
    width = len(lines[0])
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile != '.':
                initial_blizzard.add((x, y, tile))
    return initial_blizzard, height, width


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
PASS = (0, 0)

moves = {'^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT}


def get_blizzard(n, height, width, lcm):
    n = n % lcm
    if n in blizzards:
        return blizzards[n]

    previous_blizzard = get_blizzard(n - 1, height, width, lcm)
    new_blizzard = set()

    for x, y, tile in previous_blizzard:
        move = moves[tile]
        new_pos = ((x + move[0]) % width, (y + move[1]) % height, tile)
        new_blizzard.add(new_pos)

    blizzards[n] = new_blizzard
    return new_blizzard


def compute_gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def compute_lcm(x, y):
    lcm = (x*y) // compute_gcd(x, y)
    return lcm


def print_blizzard(blizzard, height, width):
    grid = [['.' for _ in range(width)] for __ in range(height)]
    for x, y, tile in blizzard:
        if grid[y][x] == '.':
            grid[y][x] = tile
        elif grid[y][x] in moves.keys():
            grid[y][x] = 2
        else:
            grid[y][x] += 1
    for line in grid:
        print(''.join(map(str, line)))


seen = set()
blizzards = {}

def can_move(blizzard, x, y):
    # Checks if the given position matches any known blizzard positions
    return not any((x, y, tile) in blizzard for tile in moves.keys())

def BFS(todo, targets, height, width, lcm):
    while todo:
        time, lap, x, y = todo.pop(0)
        target = targets[lap]
        next_blizzard = get_blizzard(time + 1, height, width, lcm)
        for step in [DOWN, RIGHT, PASS, UP, LEFT]:
            next_x, next_y = x + step[0], y + step[1]
            next_lap = lap
            if (next_x < 0 or next_y < 0 or next_x >= width or next_y >= height) and (next_x, next_y) not in targets:
                continue # don't go out of bounds
            
            if next_x == target[0] and next_y == target[1]:
                if lap == len(targets) - 1:
                    return time + 1
                next_lap = lap + 1
            next_move = (time + 1, next_lap, next_x, next_y)
            if next_move not in seen and can_move(next_blizzard, next_x, next_y):
                todo.append(next_move)
                seen.add(next_move)
    return -1

def solve(data):
    initial_blizzard, height, width = data
    lcm = compute_lcm(height, width)
    blizzards[0] = initial_blizzard
    # minute, lap, x, y
    todo = [(0, 0, 0, -1)]
    return BFS(todo, ((width - 1, height), (0, -1), (width - 1, height)), height, width, lcm)


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))

'''

'''
