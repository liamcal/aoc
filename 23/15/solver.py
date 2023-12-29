from collections import defaultdict
from functools import cache


def parse(raw_data):
    return raw_data.strip().split(',')


@cache
def do_hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


def solve1(data):
    return sum(do_hash(s) for s in data)


def solve2(data):
    hashmap = defaultdict(list)

    for instruction in data:
        if instruction[-1] == '-':
            label = instruction[:-1]
            hash = do_hash(label)
            box = hashmap[hash]
            newbox = [b for b in box if b[0] != label]
            hashmap[hash] = newbox
        else:
            label, focus = instruction[:-2], int(instruction[-1])
            hash = do_hash(label)
            box = hashmap[hash]
            if any(b[0] == label for b in box):
                newbox = [b if b[0] != label else (label, focus) for b in box]
                hashmap[hash] = newbox
            else:
                box.append((label, focus))

    ans = 0
    for k, v in hashmap.items():
        for i, (label, focus) in enumerate(v):
            ans += (k + 1) * (i + 1) * focus
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
