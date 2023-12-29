import sys

from collections import defaultdict
sys.setrecursionlimit(5000)


def parse(raw_data):
    grid = [list(line.strip()) for line in raw_data.split('\n')]
    grid_map = {}
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != '#':
                grid_map[(y, x)] = c
    return grid_map, grid


def find_neighbours(grid_map):
    neighbours = defaultdict(list)
    for position in grid_map:
        for dir in DIRS:
            neighbour = position[0] + dir[0], position[1] + dir[1]
            if neighbour in grid_map:
                neighbours[position].append(neighbour)
    return neighbours


UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
DIRS = [UP, RIGHT, DOWN, LEFT]
DIR_MAP = {'.': DIRS, '>': [RIGHT], '<': [LEFT], '^': [UP], 'v': [DOWN]}


def DFS(start, target, grid_map, use_slopes=True):
    todo = [(set([start]), start)]
    paths_to_target = []
    junctions = set()
    while todo:
        current_path, tail = todo.pop()
        if tail == target:
            paths_to_target.append(current_path)
        current_tile = grid_map[tail]
        travel_directions = DIR_MAP[current_tile] if use_slopes else DIRS
        valid_steps = 0
        for dir in travel_directions:
            next_pos = tail[0] + dir[0], tail[1] + dir[1]
            if next_pos in grid_map and next_pos not in current_path:
                new_path = current_path | set([tail])
                valid_steps += 1
                todo.append((new_path, next_pos))
        if valid_steps > 2:
            junctions.add(tail)
    return paths_to_target, junctions


def solve1(data):
    grid_map, grid = data
    start = (0, 1)
    target = (len(grid) - 1, len(grid[0]) - 2)
    paths_to_target, _ = DFS(start, target, grid_map)
    return max(len(path) for path in paths_to_target)


def find_junctions(grid_map, start):
    todo = [start]
    seen = set()
    junctions = set()
    while todo:
        pos = todo.pop(0)
        seen.add(pos)
        valid_steps = 0
        for dir in DIRS:
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if next_pos in grid_map:
                valid_steps += 1
                if next_pos not in seen:
                    todo.append(next_pos)

        if valid_steps > 2:
            junctions.add(pos)
    return junctions


def find_neighbours_for_junction(junction, junctions, grid_map):
    neighbours = []
    todo = [([junction], junction, 0)]
    seen = set([junction])
    while todo:
        path, pos, dist = todo.pop()
        seen.add(pos)
        if pos != junction and pos in junctions:
            neighbours.append((pos, dist, path))
            continue
        for dir in DIRS:
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if next_pos in grid_map and next_pos not in seen:
                new_path = path + [next_pos]
                todo.append((new_path, next_pos, dist + 1))
    return neighbours


def find_all_junction_neighbours(junctions, grid_map):
    junction_neighbours = {}
    for junction in junctions:
        junction_neighbours[junction] = find_neighbours_for_junction(
            junction, junctions, grid_map)
    return junction_neighbours

# Slow, but it get's there eventually


def solve2(data):
    grid_map, grid = data

    start = (0, 1)
    target = (len(grid) - 1, len(grid[0]) - 2)
    junctions = find_junctions(grid_map, start)
    junctions.add(start)
    junctions.add(target)

    junction_neighbours = find_all_junction_neighbours(junctions, grid_map)

    todo = [(set([(0, 1)]), (0, 1), 0, [(0, 1)])]
    max_dist = 0
    while todo:
        current_path, junction, dist, full_path = todo.pop()
        if junction == target:
            if dist > max_dist:
                max_dist = dist
        for neighbour, neighbour_dist, _ in junction_neighbours[junction]:
            if neighbour not in current_path:
                new_path = current_path | set([junction])
                todo.append((new_path, neighbour, dist +
                            neighbour_dist, full_path))
    return max_dist


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
