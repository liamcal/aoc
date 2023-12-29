def parse(raw_data):
    lines = [list(map(int, line.strip().split(' ')))
             for line in raw_data.split('\n')]
    return lines


DONE = set([0])


def find_diffs(seq):
    if set(seq) == DONE:
        return seq[0]
    diffs = [seq[i+1] - seq[i] for i in range(len(seq) - 1)]
    return find_diffs(diffs) + seq[-1]


def solve1(data):
    ans = sum(find_diffs(seq) for seq in data)
    return ans


def solve2(data):
    ans = sum(find_diffs(list(reversed(seq))) for seq in data)
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
