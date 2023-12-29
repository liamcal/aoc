import random
import networkx as nx


def parse(raw_data):
    graph = nx.Graph()  # undirected graph
    for line in raw_data.split('\n'):
        root, neighbours = line.strip().split(": ")
        neighbours = neighbours.split(" ")
        for neighbour in neighbours:
            graph.add_edge(root, neighbour, capacity=1)
    return graph


def solve1(data: nx.Graph):
    graph = data
    # keep trying until we select two nodes in different subgraphs where the min-cut is 3
    while True:
        a, b = random.choices(list(graph.nodes), k=2)
        if a != b:
            cut, (p1, p2) = nx.minimum_cut(graph, a, b)
            if cut == 3:
                return (len(p1) * len(p2))


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
