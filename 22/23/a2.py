from collections import Counter


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

search = [((-1, -1), (0, -1), (1, -1)),
          ((-1, 1), (0, 1), (1, 1)),
          ((-1, -1), (-1, 0), (-1, 1)),
          ((1, -1), (1, 0), (1, 1))]


def look(elves, pos, dir):
    try:
        val = not any((s[0] + pos[0], s[1] + pos[1])
                      in elves for s in search[dir])

    except IndexError as e:
        print("Failed to look", dir, "from", pos)
        raise e
    return val


def move(pos, dir):
    step = moves[dir]
    return pos[0] + step[0], pos[1] + step[1]


global buffer
buffer = 20


def parse_lines(lines):
    elves = []
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            if pos == '#':
                elves.append((x + buffer, y + buffer))
    return set(elves)


def solve(data):
    elves = data

    dir_offset = 0
    working = True
    while working and dir_offset < 10:
        # do shouting for one round
        shouts = {}
        for elf in elves:
            move_options = [(dir % 4, look(elves, elf, dir % 4))
                            for dir in range(dir_offset, 4 + dir_offset)]
            moves_count = sum(
                [can_move for target_dir, can_move in move_options])
            if moves_count < 4 and moves_count > 0:
                for move_option, can_move in move_options:
                    if can_move:
                        shouts[elf] = move(elf, move_option)
                        break
            else:
                shouts[elf] = None

        shout_count = Counter(shouts.values())

        # move to shout positions
        new_elves = set()
        new_elves_list = []
        working = False
        flag = False
        for elf in shouts:
            shout_target = shouts[elf]

            if shout_target is None:
                new_elves.add(elf)
                continue

            if shout_count[shout_target] == 1:
                new_elves.add(shout_target)
                new_elves_list.append(shout_target)
                working = True
            else:
                new_elves.add(elf)
                new_elves_list.append(elf)

        elves = new_elves
        dir_offset += 1
    min_x, min_y = (float('inf'), float('inf'))
    max_x, max_y = (float('-inf'), float('-inf'))

    for x, y in elves:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)


    empties = (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)
    return empties


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))

'''

'''
