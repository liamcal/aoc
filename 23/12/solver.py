from functools import cache


def parse(raw_data):
    lines = []
    for line in raw_data.split('\n'):
        springs, groups = line.strip().split(' ')
        groups = list(map(int, groups.split(',')))
        lines.append((springs, tuple(groups)))
    return lines


@cache
def find_ways(spring, sequence, in_progess=0):
    is_empty_sequence = len(sequence) == 0
    # if we've consumed all the tokens
    if len(spring) == 0:
        # 1 valid way if we've also completed consuming the sequence
        return 1 if is_empty_sequence and not in_progess else 0

    ways = 0
    head, tail = spring[0], spring[1:]

    is_current_sequence_complete = not in_progess or (
        not is_empty_sequence and sequence[0] == in_progess)

    if head == '#':
        # consume a token, increment progress for current sequence
        ways += find_ways(tail, sequence, in_progess + 1)
    elif head == '.':
        # if we haven't completed the current sequence, then prune this branch
        # otherwise, consume a token and move to the next sequence
        if is_current_sequence_complete:
            ways += find_ways(tail,
                              sequence if not in_progess else sequence[1:], 0)
    elif head == '?':
        # calculate outcomes for both possibilities
        ways += find_ways(tail, sequence, in_progess + 1)
        if is_current_sequence_complete:
            ways += find_ways(tail,
                              sequence if not in_progess else sequence[1:], 0)
    return ways


def solve1(data):
    return sum(find_ways(spring + '.', sequence) for spring, sequence in data)


def unwind_spring(spring):
    return '?'.join([spring] * 5)


def unwind_sequence(sequence):
    return sequence * 5


def solve2(data):
    return sum(find_ways(f'{unwind_spring(spring)}.{unwind_sequence(sequence)}') for spring, sequence in data)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
