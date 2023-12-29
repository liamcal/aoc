from copy import deepcopy


def parse(raw_data):
    return [[list(line.strip()) for line in grid.split('\n')] for grid in raw_data.split('\n\n')]


def transpose(grid):
    return [list(x) for x in zip(*grid)]


def find_row_reflection(grid, factor=100):
    answers = []
    for i in range(len(grid) - 1):
        above, below = grid[:i+1], grid[i+1:]
        reflection_length = min(len(above), len(below))
        above, below = above[-reflection_length:], below[:reflection_length]
        rev_b = list(reversed(below))
        if above == rev_b:
            answers.append((i + 1) * factor)
    return answers


def score_grid(grid):
    row_reflection = find_row_reflection(grid)
    if row_reflection:
        return row_reflection
    else:
        return find_row_reflection(transpose(grid), 1)


def solve1(data):
    return sum(score_grid(grid)[0] for grid in data)


def solve2(data):
    ans = 0
    for grid in data:
        initial_reflections = set(score_grid(grid))
        for y, x in ((y, x) for y in range(len(grid)) for x in range(len(grid[0]))):
            grid_c = deepcopy(grid)
            grid_c[y][x] = ('.' if grid[y][x] == '#' else '#')

            score = set(score_grid(grid_c))
            diff = score - initial_reflections
            if len(diff) == 1:
                ans += list(diff)[0]
                break

    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
