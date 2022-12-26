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



def parse_lines(lines):
    elves = set()
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            if pos == '#':
                elves.add((x, y))
    return elves


def solve(data):
    elves = data
    dir_offset = 0
    working = True
    while working:
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
        working = False
        for elf in shouts:
            shout_target = shouts[elf]

            if shout_target is None:
                new_elves.add(elf)
                continue

            if shout_count[shout_target] == 1:
                new_elves.add(shout_target)
                working = True
            else:
                new_elves.add(elf)

        elves = new_elves
        dir_offset += 1

    return dir_offset


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))

