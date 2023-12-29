from copy import deepcopy


def parse(raw_data):
    grid = [list(line.strip()) for line in raw_data.split('\n')]
    rocks = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == 'O':
                rocks.append((y, x))

    return grid, rocks


UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3


def summarize_grid(grid):
    weight = 0
    for y, line in enumerate(grid):
        for c in line:
            if c == 'O':
                weight += len(grid) - y
    return weight


def move_rocks(grid, rocks, width, height, dir):
    new_rocks = []
    if dir == UP:
        rocks = sorted(rocks, key=lambda x: x[0])
        while rocks:
            y, x = rocks.pop(0)
            grid[y][x] = '.'
            search = y
            while True:
                if search == 0 or grid[search-1][x] in ('O', '#'):
                    grid[search][x] = 'O'
                    new_rocks.append((search, x))
                    break
                search -= 1
    if dir == DOWN:
        rocks = list(reversed(sorted(rocks, key=lambda x: x[0])))
        while rocks:
            y, x = rocks.pop(0)
            grid[y][x] = '.'
            search = y
            while True:
                if search == height - 1 or grid[search+1][x] in ('O', '#'):
                    grid[search][x] = 'O'
                    new_rocks.append((search, x))
                    break
                search += 1
    if dir == LEFT:
        rocks = sorted(rocks, key=lambda x: x[1])
        while rocks:
            y, x = rocks.pop(0)
            grid[y][x] = '.'
            search = x
            while True:
                if search == 0 or grid[y][search - 1] in ('O', '#'):
                    grid[y][search] = 'O'
                    new_rocks.append((y, search))
                    break
                search -= 1
    if dir == RIGHT:
        rocks = list(reversed(sorted(rocks, key=lambda x: x[1])))
        while rocks:
            y, x = rocks.pop(0)
            grid[y][x] = '.'
            search = x
            while True:
                if search == width - 1 or grid[y][search + 1] in ('O', '#'):
                    grid[y][search] = 'O'
                    new_rocks.append((y, search))
                    break
                search += 1

    return new_rocks


def solve1(data):
    grid, rocks = data
    grid = deepcopy(grid)
    width, height = len(grid[0]), len(grid)
    move_rocks(grid, rocks, width, height, UP)
    return summarize_grid(grid)


def solve2(data):
    seen = {}
    weights = []
    grid, rocks = data
    grid = deepcopy(grid)
    width, height = len(grid[0]), len(grid)
    limit = 1_000_000_000

    for i in range(1, limit + 1):
        rocks = move_rocks(grid, rocks, width, height, UP)
        rocks = move_rocks(grid, rocks, width, height, LEFT)
        rocks = move_rocks(grid, rocks, width, height, DOWN)
        rocks = move_rocks(grid, rocks, width, height, RIGHT)

        key = ''.join(''.join(s) for s in grid)
        if key in seen:
            cycle = i - seen[key]
            sol_idx = seen[key] + (limit - seen[key]) % cycle
            return weights[sol_idx - 1]

        else:
            seen[key] = i
            weight = summarize_grid(grid)
            weights.append(weight)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
