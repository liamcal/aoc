def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    parsed = []
    for line in lines:
        c, n = line.split()
        n = int(n)
        parsed.append((c, n))
    return parsed


UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'


MOVE_MAP = {
    UP: (0, 1),
    DOWN: (0, -1),
    RIGHT: (1, 0),
    LEFT: (-1, 0)
}


def delta_pos(a, b):
    return (a[0] - b[0], a[1] - b[1])


def move_pos(a, b):
    return (a[0] + b[0], a[1] + b[1])


def isTouching(a, b):
    delta = delta_pos(a, b)
    return abs(delta[0]) <= 1 and abs(delta[1]) <= 1


def move_segment_broken(head, tail):
    # would love to debug
    relative_y, relative_x = delta_pos(head, tail)
    follow_move = (0, 0)

    if relative_y > 1:
        follow_move = (1, relative_x)
    elif relative_y < -1:
        follow_move = (-1, relative_x)
    elif relative_x > 1:
        follow_move = (relative_y, 1)
    elif relative_x < -1:
        follow_move = (relative_y, -1)

    new_tail_pos = move_pos(tail, follow_move)
    return new_tail_pos


def move_segment(head, tail):
    relative_y, relative_x = delta_pos(head, tail)
    follow_move = (0, 0)

    if not isTouching(head, tail):
        if relative_y == 0:
            follow_move = (0, 1 if relative_x > 0 else -1)
        elif relative_x == 0:
            follow_move = (1 if relative_y > 0 else -1, 0)
        else:
            for neighbor in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
                possible = move_pos(tail, neighbor)
                if isTouching(possible, head):
                    follow_move = neighbor
                    break

    new_tail_pos = move_pos(tail, follow_move)
    return new_tail_pos


def move_rope(rope_positions, initial_move):
    head_pos = rope_positions[0]
    rope_positions[0] = move_pos(head_pos, MOVE_MAP[initial_move])
    for segment in range(1, len(rope_positions)):
        rope_positions[segment] = move_segment(
            rope_positions[segment-1], rope_positions[segment])
    return rope_positions


ROPE_SIZE = 10
tail_visited = set()


def solve(parsed_lines):
    rope_positions = [(0, 0) for _ in range(ROPE_SIZE)]
    tail_visited.add(rope_positions[-1])

    for instruction in parsed_lines:
        direction, steps = instruction
        for _ in range(steps):
            rope_positions = move_rope(rope_positions, direction)
            tail_visited.add(rope_positions[-1])

    return len(tail_visited)


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
