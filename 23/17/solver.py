import heapq as heap
from collections import defaultdict


DOWN, UP, RIGHT, LEFT = (1, 0), (-1, 0), (0, 1), (0, -1)
DIRS = [DOWN, UP, RIGHT, LEFT]


def get_possible_dirs(dir):
    return [d for d in DIRS if d != (dir[0] * -1, dir[1] * -1)]


def dijkstra1(grid, startingNode):
    height, width = len(grid), len(grid[0])
    visited = set()
    parents = {}
    pq = []
    costs = defaultdict(lambda: float('inf'))
    costs[startingNode] = 0
    heap.heappush(pq, (0, startingNode))

    while pq:
        _, node = heap.heappop(pq)
        visited.add(node)

        pos, cur_dir, dir_steps = node
        for new_dir in get_possible_dirs(cur_dir):
            new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
            y, x = new_pos
            if y < 0 or y >= height or x < 0 or x >= width:
                continue
            new_steps = 1 if new_dir != cur_dir else dir_steps + 1
            if new_steps > 3:
                continue
            new_node = new_pos, new_dir, new_steps
            if new_node in visited:
                continue
            new_weight = grid[y][x]
            new_total = costs[node] + new_weight
            if costs[new_node] > new_total:
                parents[new_node] = node
                costs[new_node] = new_total
                heap.heappush(pq, (new_total, new_node))
    return parents, costs


def dijkstra2(grid, start_node):
    height, width = len(grid), len(grid[0])
    visited = set()
    parents = {}
    pq = []
    costs = defaultdict(lambda: float('inf'))
    costs[start_node] = 0
    heap.heappush(pq, (0, start_node))
    target = (height - 1, width - 1)
    while pq:
        _, node = heap.heappop(pq)
        visited.add(node)

        pos, cur_dir, dir_steps = node
        for new_dir in get_possible_dirs(cur_dir):
            if dir_steps < 4 and new_dir != cur_dir and dir_steps > 0:
                continue
            new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
            y, x = new_pos
            if y < 0 or y >= height or x < 0 or x >= width:
                continue
            new_steps = 1 if new_dir != cur_dir else dir_steps + 1
            if new_steps > 10:
                continue
            new_node = new_pos, new_dir, new_steps

            if new_node in visited:
                continue
            new_weight = grid[y][x]
            new_total = costs[node] + new_weight

            if new_pos == target:
                if new_steps < 4:
                    continue

            if costs[new_node] > new_total:
                parents[new_node] = node
                costs[new_node] = new_total
                heap.heappush(pq, (new_total, new_node))

    return parents, costs


def parse(raw_data):
    return [list(map(int, list(line.strip()))) for line in raw_data.split('\n')]


def solve1(data):
    _, costs = dijkstra1(data, ((0, 0), RIGHT, 0))
    full_path = [p for p in costs.keys() if p[0] == (
        len(data) - 1, len(data[0]) - 1)][0]
    return (costs[full_path])


def solve2(data):
    _, costs = dijkstra2(data, ((0, 0), DOWN, 0))
    full_path = [p for p in costs.keys() if p[0] == (
        len(data) - 1, len(data[0]) - 1) and p[2] >= 4]

    return costs[full_path[0]]


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
