from math import lcm


def parse(raw_data):
    lines = [line.strip() for line in raw_data.split('\n') if line]
    sequence, nodes = lines[0], lines[1:]
    sequence = [1 if c == 'R' else 0 for c in sequence]

    network = {}
    for node in nodes:
        node_name, paths = node.split(' = ')
        network[node_name] = (paths[1:4], paths[6:9])

    return sequence, network


def walk_network(sequence, network, start_positions):
    i = 0
    done = []
    positions = start_positions
    while True:
        cur_instruction = sequence[i % len(sequence)]
        next_positions = []
        for position in positions:
            next_position = network[position][cur_instruction]
            if next_position[-1] == 'Z':
                done.append(i + 1)
            else:
                next_positions.append(next_position)

        if next_positions:
            positions = next_positions
        else:
            break
        i += 1
    ans = lcm(*done)
    return ans


def solve1(data):
    sequence, network = data
    start_position = 'AAA'
    return walk_network(sequence, network, [start_position])


def solve2(data):
    sequence, network = data
    start_positions = [i for i in network.keys() if i[-1] == 'A']
    return walk_network(sequence, network, start_positions)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
