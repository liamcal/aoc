def parse(raw_data):
    return [line.strip().split(':') for line in raw_data.split('\n')]


# PART 1
def solve1(data):
    limits = {'red': 12, 'blue': 14, 'green': 13}

    ans = 0

    for game, rounds in data:
        g_id = int(game.split()[1])
        rounds = rounds.strip().split(';')
        for r in rounds:
            seen = {'red': 0, 'blue': 0, 'green': 0}
            blocks = r.strip().split(',')
            for block in blocks:
                n, color = block.strip().split(' ')
                n = int(n)
                seen[color] = seen[color] + n
            if any(seen[color] > limits[color] for color in seen.keys()):
                break
        else:
            ans += g_id
    return ans


# PART 2
def solve2(data):
    ans = 0

    for game, rounds in data:
        rounds = rounds.strip().split(';')
        required = {'red': 0, 'blue': 0, 'green': 0}
        for r in rounds:
            seen = {'red': 0, 'blue': 0, 'green': 0}
            blocks = r.strip().split(',')
            for block in blocks:
                n, color = block.strip().split(' ')
                n = int(n)
                seen[color] = seen[color] + n
            for k in required:
                required[k] = max(required[k], seen[k])
        power = 1
        for k in required:
            power *= required[k]
        ans += power

    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
