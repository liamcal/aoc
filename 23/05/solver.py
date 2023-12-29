import math


class SeedMapper:
    def __init__(self, id: int):
        self.id = id
        self.rows = []

    def add_row(self, dest_start: int, source_start: int, range_len: int):
        self.rows.append((dest_start, source_start, range_len))

    def is_handled_by_row(self, val, source_start, range_len):
        return val >= source_start and val < source_start + range_len

    def lookup(self, val: int):
        for dest_start, source_start, range_len in self.rows:
            if self.is_handled_by_row(val, source_start, range_len):
                return dest_start + (val - source_start)
        return val

    def reverse_lookup(self, val: int):
        for dest_start, source_start, range_len in self.rows:
            if self.is_handled_by_row(val, dest_start, range_len):
                return source_start + (val - dest_start)
        return val


def parse(raw_data):
    sections = [line.strip() for line in raw_data.split('\n\n')]
    seeds = list(map(int, sections[0].split(':')[1].strip().split(' ')))
    return seeds, [section.split('\n')[1:] for section in sections[1:]]


def solve1(data):
    seed_maps = []

    seeds, seed_map_datas = data
    for i, seed_map_data in enumerate(seed_map_datas):
        seed_map = SeedMapper(i)
        seed_maps.append(seed_map)

        for line in seed_map_data:
            dest_start, source_start, range_len = list(
                map(int, line.split(' ')))
            seed_map.add_row(dest_start, source_start, range_len)

    locations = []
    for seed in seeds:
        current_id = seed
        for seed_map in seed_maps:
            current_id = seed_map.lookup(current_id)
        locations.append(current_id)
    least_location = min(location for location in locations)
    return least_location


def solve2_manual(data):
    # There are just too many seeds to solve this one by brute force like this in a sensible amount of time
    # A better solution would be to use intervals (below), but we can still use brute force if we cut the sample space enough
    # So first, let's search over every nth seed where n is a reasonably large number (start with square-root of total seed count)
    # That should give us an approximate answer which is *hopefully* in the same seed range as the true answer
    # A quick calculation can then find that initial seed range
    # Finally, brute over only that seed range, logging whenever we find a new candidate answer
    # There is a decent chance once new potential solutions settle, we might have reached the true answer, so try submitting while everything keeps running
    # Another aside, this seems like a good candidate for multithreaded computation, but python GIL says no

    # Control variables
    INITIAL_PASS = False
    # Put the seed found from the initial pass e.g 3352513378
    FIND_RANGE_FOR_SEED = None
    # 2-tuple of seed range found that contains initial candidate e.g 3419921504, 53335682
    RANGE_OVERRIDE = None

    seeds, seed_map_datas = data
    seed_groups = list(zip(*(iter(seeds),) * 2))

    if FIND_RANGE_FOR_SEED is not None:
        for seed_start, seed_range in seed_groups:
            if FIND_RANGE_FOR_SEED >= seed_start and FIND_RANGE_FOR_SEED < seed_start + seed_range:
                return seed_start, seed_range

    seed_groups_to_evaluate = [
        RANGE_OVERRIDE] if RANGE_OVERRIDE is not None else seed_groups

    all_seeds = []
    for seed_start, seed_range in seed_groups_to_evaluate:
        all_seeds.extend(range(seed_start, seed_start + seed_range))

    seed_maps = []

    for i, seed_map_data in enumerate(seed_map_datas):
        seed_map = SeedMapper(i)
        seed_maps.append(seed_map)

        for line in seed_map_data:
            dest_start, source_start, range_len = list(
                map(int, line.split(' ')))
            seed_map.add_row(dest_start, source_start, range_len)

    seed_count = len(all_seeds)
    n = int(math.sqrt(seed_count)) if INITIAL_PASS else 1

    least_location = None
    least_seed = None
    for i in range(0, seed_count + 1, n):
        seed = all_seeds[i]
        current_id = seed
        for seed_map in seed_maps:
            new_id = seed_map.lookup(current_id)
            current_id = new_id
        if least_location is None or current_id < least_location:
            print("Seed", seed, '->', "Location", current_id, '--', i)
            least_location = current_id
            least_seed = seed

        # Just to monitor things are actually running
        # if i % 1000000 == 0:
        #     print("Periodic update", i, least_location, least_seed)

    return least_location, least_seed


def is_in_seed_groups(i, seed_groups):
    for start, r in seed_groups:
        if start <= i and i < start + r:
            return True
    return False


def solve2_backwards(data):
    # Brute force, but do it in reverse
    # i.e try potential ending locations and work through the maps backwards
    # the first location we find that reverse maps to one of the seed values will be the smallest location
    # still takes 10s of minutes to complete, but it does complete and doesn't require manual tweaking

    seeds, seed_map_datas = data
    seed_groups = list(zip(*(iter(seeds),) * 2))

    seed_maps = []
    for i, seed_map_data in enumerate(seed_map_datas):
        seed_map = SeedMapper(i)
        seed_maps.append(seed_map)

        for line in seed_map_data:
            dest_start, source_start, range_len = list(
                map(int, line.split(' ')))
            seed_map.add_row(dest_start, source_start, range_len)
    least_location = None
    least_seed = None
    i = 1
    while True:
        current_id = i
        for seed_map in reversed(seed_maps):
            new_id = seed_map.reverse_lookup(current_id)
            current_id = new_id
        if is_in_seed_groups(current_id, seed_groups):
            print("Found answer", i, current_id)
            break

        # Just to monitor things are actually running
        if i % 10000000 == 0:
            print("Periodic update", i, least_location, least_seed)
        i += 1

    return i


# Intervals are hard but we got there in the end
def locate_range_in_map(seed_ranges, seed_map):
    todo = []  # chunks handled by map
    ranges_to_check = seed_ranges[:]

    i = 0
    for map_dest, map_src, map_len in seed_map:
        range_start, range_end = map_src, map_src + map_len
        new_ranges = []
        for seed_start, seed_end in ranges_to_check:
            # Entirely before or after
            if seed_end < range_start or seed_start > range_end:
                new_ranges.append((seed_start, seed_end))

            # Overlap on left and right
            elif seed_start <= range_start and seed_end > range_end:
                # left chunk
                new_ranges.append((seed_start, range_start))
                # middle chunk
                todo.append((map_dest, map_dest + range_end - range_start))
                # right chunk
                new_ranges.append((range_end, seed_end))

            # Seeds overlap on left
            elif seed_start < range_start and seed_end > range_start:
                # left chunk
                new_ranges.append((seed_start, range_start))
                # middle chunk
                todo.append((map_dest, map_dest + seed_end - range_start))

            # seeds overlap on right
            elif seed_start < range_end and seed_end > range_end:
                # middle chunk
                todo.append((map_dest + seed_start - range_start,
                            map_dest + range_end - range_start))
                # right chunk
                new_ranges.append((range_end, seed_end))

            # range contains seeds entirely
            elif seed_start >= range_start and seed_end <= range_end:
                todo.append((map_dest + seed_start - range_start,
                            map_dest + seed_end - range_start))

        ranges_to_check = new_ranges[:]
        i += 1
    return todo + ranges_to_check


def solve2(data):
    seeds, seed_map_datas = data
    seed_groups = [(seed_start, seed_start + seed_len)
                   for seed_start, seed_len in (zip(*(iter(seeds),) * 2))]
    seed_maps = []
    for seed_map_data in seed_map_datas:
        seed_map = []

        for line in seed_map_data:
            dest_start, source_start, range_len = list(
                map(int, line.split(' ')))
            seed_map.append((dest_start, source_start, range_len))
        seed_maps.append(seed_map)

    current_seed_groups = seed_groups
    for seed_map in seed_maps:
        new_seed_groups = locate_range_in_map(current_seed_groups, seed_map)
        current_seed_groups = new_seed_groups
    return min(g[0] for g in current_seed_groups)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
