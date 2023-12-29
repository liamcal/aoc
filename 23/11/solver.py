from itertools import combinations


def parse(raw_data):
    return [list(line.strip()) for line in raw_data.split('\n')]


def expand_universe(grid):
    new_galaxy = []
    # expand horizontally
    for line in grid:
        new_galaxy.append(line)
        if all(c == '.' for c in line):
            new_galaxy.append(line)
    # expand vertically
    vertical_expands = []
    for i in range(len(grid[0])):
        if all(grid[y][i] == '.' for y in range(len(grid))):
            vertical_expands.append(i)
    new_new_galaxy = []
    for line in new_galaxy:
        new_line = []
        for i, c in enumerate(line):
            new_line.append(c)
            if i in vertical_expands:
                new_line.append('.')
        new_new_galaxy.append(new_line)
    return new_new_galaxy


def find_expansion_points(grid):
    horizontal_expansions = []
    # expand horizontally
    for i, line in enumerate(grid):
        if all(c == '.' for c in line):
            horizontal_expansions.append(i)
    # expand vertically
    vertical_expansions = []
    for i in range(len(grid[0])):
        if all(grid[y][i] == '.' for y in range(len(grid))):
            vertical_expansions.append(i)

    return horizontal_expansions, vertical_expansions


def find_galaxies(grid):
    galaxies = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((y, x))
    return galaxies


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve1(data):
    expanded = expand_universe(data)
    galaxies = find_galaxies(expanded)
    pairs = list(combinations(galaxies, 2))
    ans = 0
    for a, b in pairs:
        ans += manhattan(a, b)
    return ans


def add_expansion(horizontal_expansions, vertical_expansions, a, b, exp_factor):
    expansion_dist = 0
    y_min, y_max = min(a[0], b[0]), max(a[0], b[0])
    x_min, x_max = min(a[1], b[1]), max(a[1], b[1])
    for h in horizontal_expansions:
        if y_min < h and h < y_max:
            expansion_dist += exp_factor
    for v in vertical_expansions:
        if x_min < v and v < x_max:
            expansion_dist += exp_factor
    return expansion_dist


def solve2(data):
    horizontal_expansions, vertical_expansions = find_expansion_points(data)
    galaxies = find_galaxies(data)
    pairs = list(combinations(galaxies, 2))
    ans = 0
    for a, b in pairs:
        ans += manhattan(a, b)
        ans += add_expansion(horizontal_expansions,
                             vertical_expansions, a, b, 999999)
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
