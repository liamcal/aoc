import numpy as np


UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)


def get_dir(s):
    if s == 'R':
        return RIGHT
    if s == 'L':
        return LEFT
    if s == 'U':
        return UP
    if s == 'D':
        return DOWN


def parse(raw_data):
    grid = [line.strip().split() for line in raw_data.split('\n')]
    return grid


def solve1(data):
    return solve(((get_dir(dir), int(dist)) for dir, dist, _ in data), True)


def get_dir_from_hex(hex_dir):
    if hex_dir == '0':
        return RIGHT
    if hex_dir == '1':
        return DOWN
    if hex_dir == '2':
        return LEFT
    if hex_dir == '3':
        return UP


def shoelace(xs, ys):
    x = np.array(xs)
    y = np.array(ys)
    i = np.arange(len(x))
    return np.abs(np.sum(x[i-1] * y[i] - x[i] * y[i-1]) * 0.5)


def solve(data):
    pos = (0, 0)
    perimeter = 0
    xs = []
    ys = []

    for dir, dist in data:
        new_pos = pos[0] + (dir[0] * dist), pos[1] + (dir[1] * dist)
        ys.append(new_pos[0])
        xs.append(new_pos[1])
        perimeter += dist
        pos = new_pos

    return int(shoelace(xs, ys)) + (perimeter // 2) + 1


def solve2(data):
    return solve(((get_dir_from_hex(hex[7]), int(hex[2:7], 16)) for _, __, hex in data))


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
