

def read_file(filename = 'in.txt'):
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

def move_rope(head_pos, tail_pos, dir):
    relative = delta_pos(head_pos, tail_pos)
    new_head_pos = move_pos(head_pos, MOVE_MAP[dir])
    new_tail_pos = tail_pos

    if relative == (0, 0):
        pass
    elif relative == (0, 1):
        ## U
        if dir == UP:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[UP])
    elif relative == (0, -1):
        ## D
        if dir == DOWN:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[DOWN])
    elif relative == (1, 0):
        ## R
        if dir == RIGHT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[RIGHT])
    elif relative == (-1, 0):
        ## L
        if dir == LEFT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[LEFT])
    elif relative == (1, 1):
        ## UR
        if dir == UP or dir == RIGHT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[UP])
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[RIGHT])
    elif relative == (1, -1):
        ## DR
        if dir == DOWN or dir == RIGHT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[DOWN])
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[RIGHT])
    elif relative == (-1, 1):
        ## UL
        if dir == UP or dir == LEFT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[UP])
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[LEFT])
    elif relative == (-1, -1):
        ## DL
        if dir == DOWN or dir == LEFT:
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[DOWN])
            new_tail_pos = move_pos(new_tail_pos, MOVE_MAP[LEFT])
    return (new_head_pos, new_tail_pos)

tail_visited = set()
def solve(parsed_lines):
    head_pos = (0, 0)
    tail_pos = (0, 0)
    tail_visited.add(tail_pos)
    for instruction in parsed_lines:
        direction, steps = instruction
        for _ in range(steps):
            head_pos, tail_pos = move_rope(head_pos, tail_pos, direction)
            tail_visited.add(tail_pos)
        
    return len(tail_visited)

if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))

