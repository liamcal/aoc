from collections import defaultdict
from functools import cache


def parse(raw_data):
    lines = [line.strip() for line in raw_data.split('\n')]
    out = []
    for line in lines:
        a, b = line.split('~')
        a, b = tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))
        out.append((a, b))
    return out


def overlaps_xy(a, b):
    a_min_x, a_max_x = min(a[0][0], a[1][0]),  max(a[0][0], a[1][0])
    a_min_y, a_max_y = min(a[0][1], a[1][1]),  max(a[0][1], a[1][1])

    b_min_x, b_max_x = min(b[0][0], b[1][0]),  max(b[0][0], b[1][0])
    b_min_y, b_max_y = min(b[0][1], b[1][1]),  max(b[0][1], b[1][1])
    return (
        (
            a_min_x <= b_min_x <= a_max_x or a_min_x <= b_max_x <= a_max_x or
            b_min_x <= a_min_x <= b_max_x or b_min_x <= a_max_x <= b_max_x
        ) and (
            a_min_y <= b_min_y <= a_max_y or a_min_y <= b_max_y <= a_max_y or
            b_min_y <= a_min_y <= b_max_y or b_min_y <= a_max_y <= b_max_y
        )
    )


@cache
def fall(area, n=1):
    return (area[0][0], area[0][1], area[0][2] - n), (area[1][0], area[1][1], area[1][2] - n)


def fall_all(min_lookup, max_lookup):
    moved = True
    while moved:
        moved = False
        for z, z_bricks in sorted(min_lookup.items()):
            if z <= 1:
                continue

            for brick in list(z_bricks):
                if not any(overlaps_xy(brick, other_brick) for other_brick in max_lookup[z-1]):
                    min_lookup[min(brick[0][2], brick[1][2])].remove(brick)
                    max_lookup[max(brick[0][2], brick[1][2])].remove(brick)
                    fallen_brick = fall(brick)
                    min_lookup[min(fallen_brick[0][2], fallen_brick[1][2])].append(
                        fallen_brick)
                    max_lookup[max(fallen_brick[0][2], fallen_brick[1][2])].append(
                        fallen_brick)
                    moved = True
    new_bricks = []
    for bl in min_lookup.values():
        new_bricks.extend(bl)
    return new_bricks


def solve1(data):
    bricks = data
    min_lookup = defaultdict(list)
    max_lookup = defaultdict(list)
    for brick in bricks:
        min_lookup[min(brick[0][2], brick[1][2])].append(brick)
        max_lookup[max(brick[0][2], brick[1][2])].append(brick)
    fall_all(min_lookup, max_lookup)

    disintegrated = []
    for z, z_bricks in sorted(max_lookup.items()):
        # for each brick maxz..
        for brick in z_bricks:
            max_z = max(brick[0][2], brick[1][2])

            # find which bricks it's supporting
            bricks_above = min_lookup[max_z + 1]
            supporting = [
                other_brick for other_brick in bricks_above if overlaps_xy(brick, other_brick)]
            # if nothing, we can disintegrate
            if not supporting:
                disintegrated.append(brick)
                continue

            # for each brick we're supporting, see how many bricks support it
            needed = False
            for target_brick in supporting:
                min_z = min(target_brick[0][2], target_brick[1][2])

                bricks_below_target = max_lookup[min_z-1]
                supported_by = [other_brick for other_brick in bricks_below_target if overlaps_xy(
                    target_brick, other_brick)]
                # if only 1, b is essential
                if len(supported_by) == 1:
                    assert supported_by[0] == brick
                    needed = True
                    break

            if not needed:
                disintegrated.append(brick)

    return len(disintegrated)


def solve2(data):
    bricks = data
    min_lookup = defaultdict(list)
    max_lookup = defaultdict(list)
    for brick in bricks:
        min_lookup[min(brick[0][2], brick[1][2])].append(brick)
        max_lookup[max(brick[0][2], brick[1][2])].append(brick)
    bricks = fall_all(min_lookup, max_lookup)
    ans = 0
    supporting = {}
    supported_by = {}
    for brick in bricks:
        supporting[brick] = set(
            [supporting_brick for supporting_brick in min_lookup[max(brick[0][2], brick[1][2])+1] if overlaps_xy(brick, supporting_brick)])
        supported_by[brick] = set(
            [supported_brick for supported_brick in max_lookup[min(brick[0][2], brick[1][2])-1] if overlaps_xy(brick, supported_brick)])

    for brick in bricks:
        todo = [brick]
        falling = set(todo)

        while todo:
            current_brick = todo.pop()
            for supporting_brick in supporting[current_brick]:

                if supported_by[supporting_brick].issubset(falling):
                    falling.add(supporting_brick)
                    todo.append(supporting_brick)

        ans += len(falling - 1)  # current brick doesn't fall
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
