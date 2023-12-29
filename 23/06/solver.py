from numpy import roots
import math
import re


def parse_line(line):
    return list(map(int, re.split(r'\s+', line.split(':')[1].strip())))


def parse(raw_data):
    lines = [line.strip() for line in raw_data.split('\n')]
    times = parse_line(lines[0])
    distances = parse_line(lines[1])
    return list(zip(times, distances))


def distance_travelled(hold_time, max_time):
    return (max_time - hold_time) * hold_time


def solve1(data):
    ans = 1
    for time, distance in data:
        zeroes = roots([-1, time, -1*distance])
        ans *= abs(math.floor(zeroes[0]) - math.floor(zeroes[1]))
    return ans


def solve2(data):
    actual_time = int(''.join((str(time) for time, dist in data)))
    actual_distance = int(''.join((str(dist) for time, dist in data)))

    ans = 1
    zeroes = roots([-1, actual_time, -1*actual_distance])
    ans *= abs(math.floor(zeroes[0]) - math.floor(zeroes[1]))
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
