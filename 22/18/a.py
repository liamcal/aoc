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


def solve(parsed_lines):
    adjacencies = [(-1, 0, 0), (1, 0, 0), (0, -1, 0),
                   (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    cubes = parsed_lines
    total = 0

    for cube in cubes:
        for adjacent in adjacencies:
            if add_coord(cube, adjacent) not in cubes:
                total += 1
    return total


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
