from itertools import product


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    cubes = set()
    for line in lines:
        x, y, z = map(int, line.split(','))
        cubes.add((x, y, z))
    return cubes


def add_coord(a, b):
    return tuple(sum(x) for x in zip(a, b))


global MIN, MAX
# taken based on a visual scan of the input
MIN = -3
MAX = 20


def solve(parsed_lines):
    adjacencies = [(-1, 0, 0), (1, 0, 0), (0, -1, 0),
                   (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    cubes = parsed_lines
    total = 0
    water = set()
    start_pos = (MIN, MIN, MIN)
    todo = [start_pos]
    while todo:
        current = todo.pop(0)
        next_batch = []
        for adjacent in adjacencies:
            inspecting = add_coord(current, adjacent)
            if all(p >= MIN and p <= MAX for p in inspecting) and inspecting not in cubes and inspecting not in water:
                water.add(inspecting)
                next_batch.append(inspecting)
        todo = todo + next_batch
    for cube in cubes:
        for adjacent in adjacencies:
            inspecting = add_coord(cube, adjacent)

            if inspecting in water:
                total += 1

    return total


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
