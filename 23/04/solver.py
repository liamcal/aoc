import re


def parse(raw_data):
    return [line.strip() for line in raw_data.split('\n')]


def solve1(data):
    ans = 0
    for line in data:
        card, numbers = line.split(':')
        numbers = numbers.strip()
        winning, mine = numbers.split('|')
        winning, mine = set(map(int, re.split(r'\s+', winning.strip()))
                            ), set(map(int, re.split(r'\s+', mine.strip())))
        matches = len(mine.intersection(winning))
        if matches:
            ans += 2 ** (matches - 1)
    return ans


def solve2(data):
    line_count = len(data)

    card_count = {i: 1 for i in range(line_count)}

    for i, line in enumerate(data):
        card, numbers = line.split(':')
        numbers = numbers.strip()
        winning, mine = numbers.split('|')
        winning, mine = set(map(int, re.split(r'\s+', winning.strip()))
                            ), set(map(int, re.split(r'\s+', mine.strip())))
        matches = len(mine.intersection(winning))
        for j in range(i+1, i+1+matches):
            card_count[j] += card_count[i]

    return sum(card_count[card] for card in card_count)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
