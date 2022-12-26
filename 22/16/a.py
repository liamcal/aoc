from itertools import product
from collections import defaultdict


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def floyd_warshall(g):
    distance = {x: {y: float('inf') for y in g.keys()} for x in g.keys()}

    for a, bs in g.items():
        distance[a][a] = 0

        for b in bs:
            distance[a][b] = 1
            distance[b][b] = 0

    for a, b, c in product(g, g, g):
        bc, ba, ac = distance[b][c], distance[b][a], distance[a][c]

        if ba + ac < bc:
            distance[b][c] = ba + ac

    return distance


def parse_lines(lines):
    graph = defaultdict(list)
    rates = {}

    for line in lines:
        fields = line.split()
        src = fields[1]
        distances = list(map(lambda x: x.rstrip(','), fields[9:]))
        rate = int(fields[4][5:-1])

        rates[src] = rate

        for d in distances:
            graph[src].append(d)
    return graph, rates


def score(rates, chosen_valves):
    return sum(rates[valve] * time_left for valve, time_left in chosen_valves.items())


def DFS(current_valve, distances, valves, time, chosen={}):
    for next_valve in valves:
        new_valves = valves - {next_valve}
        # Choosing this valve will take distance[cur][nxt] to reach it 1m to open it
        time_to_open = distances[current_valve][next_valve] + 1
        new_time = time - time_to_open

        if new_time < 1:
            continue
        new_chosen = chosen | {next_valve: new_time}
        yield from DFS(next_valve, distances, new_valves, new_time, new_chosen)
    yield chosen


START_VALUE = 'AA'
TIME_AVAILABLE = 30


def solve(data):
    graph, rates = data
    good = frozenset(filter(rates.get, graph))
    distances = floyd_warshall(graph)

    best = max(score(rates, s)
               for s in DFS(START_VALUE, distances, good, TIME_AVAILABLE))

    return best


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
