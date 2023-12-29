LEFT, UP, DOWN, RIGHT = (0, -1), (-1, 0), (1, 0), (0, 1)


def parse(raw_data):
    return [list(line.strip()) for line in raw_data.split('\n')]


def energize(grid, height, width, start_beam):
    seen = set()
    beams = [start_beam]
    energized = set()
    while beams:
        beam = beams.pop(0)
        if beam in seen:
            continue
        seen.add(beam)
        pos, dir = beam
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if new_pos[0] >= 0 and new_pos[0] < height and new_pos[1] >= 0 and new_pos[1] < width:
            energized.add(new_pos)
            next_token = grid[new_pos[0]][new_pos[1]]
            if next_token == '.':
                beams.append((new_pos, dir))
            if next_token == '/':
                if dir == DOWN:
                    new_dir = LEFT
                elif dir == LEFT:
                    new_dir = DOWN
                elif dir == UP:
                    new_dir = RIGHT
                elif dir == RIGHT:
                    new_dir = UP
                beams.append((new_pos, new_dir))
            elif next_token == '\\':
                if dir == DOWN:
                    new_dir = RIGHT
                elif dir == RIGHT:
                    new_dir = DOWN
                elif dir == UP:
                    new_dir = LEFT
                elif dir == LEFT:
                    new_dir = UP
                beams.append((new_pos, new_dir))
            elif next_token == '-':
                if dir in (LEFT, RIGHT):
                    beams.append((new_pos, dir))
                elif dir in (UP, DOWN):
                    beams.append((new_pos, LEFT))
                    beams.append((new_pos, RIGHT))
            elif next_token == '|':
                if dir in (UP, DOWN):
                    beams.append((new_pos, dir))
                elif dir in (LEFT, RIGHT):
                    beams.append((new_pos, UP))
                    beams.append((new_pos, DOWN))
    return len(energized)


def solve1(data):
    height, width = len(data), len(data[0])
    return energize(data, height, width, (((height//2)//2, width), LEFT, 0))


def solve2(data):
    height, width = len(data), len(data[0])
    ans = 0
    for i in range(height):
        ans = max(ans, energize(data, height, width, ((i, -1), RIGHT)))
        ans = max(ans, energize(data,  height, width, ((i, width), LEFT)))

    for i in range(width):
        ans = max(ans, energize(data, height, width, ((-1, i), DOWN)))
        ans = max(ans, energize(data,  height, width, ((height, i), UP)))
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
