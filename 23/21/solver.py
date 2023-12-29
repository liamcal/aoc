import numpy as np


def parse(raw_data):
    grid = [list(line.strip()) for line in raw_data.split('\n')]
    start = None
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == 'S':
                start = (y, x)
                grid[y][x] = '.'
    return grid, start


UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
DIRS = [UP, RIGHT, DOWN, LEFT]


def solve1(data):
    grid, start = data
    height, width = len(grid), len(grid[0])
    todo = {start}
    for step in range(64):
        new_todo = set()
        for y, x in todo:
            for dy, dx in DIRS:
                new_y, new_x = y + dy, x + dx
                if new_y >= 0 and new_y < height and new_x >= 0 and new_x < width and grid[new_y][new_x] != '#':
                    new_todo.add((new_y, new_x))
        todo = new_todo
    return len(new_todo)


def solve2(data):
    grid, start = data

    height, width = len(grid), len(grid[0])
    todo = {start}
    targets = {height // 2, height // 2 + height, height // 2 + 2 * height}
    ys = []
    # ys = [3847, 34165, 94697]
    total = 26501365
    step = 1
    while len(ys) != len(targets):
        new_todo = set()
        for y, x in todo:
            for dy, dx in DIRS:
                new_y, new_x = y + dy, x + dx
                if grid[new_y % height][new_x % width] != '#':
                    new_todo.add((new_y, new_x))
        todo = new_todo
        if step in targets:
            ys.append(len(todo))

        step += 1

    a, b, c = map(round, np.polyfit(range(3), ys, 2))
    x = (total - total % height) // height
    return (a * x**2) + (b * x) + c


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
