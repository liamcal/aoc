

from collections import defaultdict


def parse(raw_data):
    return [list(line.strip()) for line in raw_data.split('\n')]


# PART 1
def solve1(data):
    grid = data
    y_min, x_min = 0, 0
    y_max, x_max = len(grid), len(grid[0])
    ans = 0

    def is_symbol(y, x):
        if y < y_min or y >= y_max or x < x_min or x >= x_max:
            return False
        value = grid[y][x]
        return not (value.isdigit() or value == '.')

    for y, line in enumerate(grid):
        is_num = False
        num_start = -1
        num_end = -1
        num = ''
        for x, item in enumerate(line):
            if not is_num:
                if not item.isdigit():
                    continue
                is_num = True
                num_start = x
                num += item
            else:
                if item.isdigit():
                    num += item
                    continue
                is_num = False
                num_end = x
                num = int(num)
                if any(is_symbol(y-1, x_check) for x_check in range(num_start-1, num_end+1)) or \
                        any(is_symbol(y+1, x_check) for x_check in range(num_start-1, num_end+1)) or \
                        is_symbol(y, num_start-1) or is_symbol(y, num_end):
                    ans += num

                is_num = False
                num_start = -1
                num_end = -1
                num = ''
        if is_num:
            is_num = False
            num_end = x + 1
            num = int(num)
            if any(is_symbol(y-1, x_check) for x_check in range(num_start-1, num_end+1)) or \
                    any(is_symbol(y+1, x_check) for x_check in range(num_start-1, num_end+1)) or \
                    is_symbol(y, num_start-1) or is_symbol(y, num_end):
                ans += num

            is_num = False
            num_start = -1
            num_end = -1
            num = ''
    return ans


# PART 2
def solve2(data):
    grid = data
    y_min, x_min = 0, 0
    y_max, x_max = len(grid), len(grid[0])
    ans = 0

    def is_gear(y, x):
        if y < y_min or y >= y_max or x < x_min or x >= x_max:
            return None
        value = grid[y][x]
        return (y, x) if value == '*' else None

    gear_map = defaultdict(list)

    for y, line in enumerate(grid):
        is_num = False
        num_start = -1
        num_end = -1
        num = ''
        for x, item in enumerate(line):
            if not is_num:
                if not item.isdigit():
                    continue
                is_num = True
                num_start = x
                num += item
            else:
                if item.isdigit():
                    num += item
                    continue
                is_num = False
                num_end = x
                num = int(num)
                gears = [is_gear(y-1, x_check) for x_check in range(num_start-1, num_end+1)] + \
                        [is_gear(y+1, x_check) for x_check in range(num_start-1, num_end+1)] + \
                        [is_gear(y, num_start-1)] + [is_gear(y, num_end)]
                gears = [g for g in gears if g is not None]
                if (gears):
                    gear_map[gears[0]].append(num)

                is_num = False
                num_start = -1
                num_end = -1
                num = ''
        if is_num:
            is_num = False
            num_end = x + 1
            num = int(num)
            gears = [is_gear(y-1, x_check) for x_check in range(num_start-1, num_end+1)] + \
                    [is_gear(y+1, x_check) for x_check in range(num_start-1, num_end+1)] + \
                    [is_gear(y, num_start-1)] + [is_gear(y, num_end)]
            gears = [g for g in gears if g is not None]
            if (gears):
                gear_map[gears[0]].append(num)

            is_num = False
            num_start = -1
            num_end = -1
            num = ''

    for gear in gear_map:
        if len(gear_map[gear]) == 2:
            ratio = gear_map[gear][0] * gear_map[gear][1]
            ans += ratio

    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
