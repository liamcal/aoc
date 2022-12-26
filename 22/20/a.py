def read_file(filename = 'in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_lines(lines):
    items = []
    for i, line in enumerate(lines):
        items.append((i, int(line)))    
    return items        

def solve(data):
    # print([d[1] for d in data])
    width = len(data)
    for step in range(width):
        pos = None
        for i, item in enumerate(data):
            if item[0] == step:
                pos = i
                break
        target = data.pop(pos)
        value = target[1]
        new_pos = (pos + value) % (width - 1)
        if new_pos == 0:
            data.append(target)
        else:
            data.insert(new_pos, target)
        # print([d[1] for d in data])
    results = [d[1] for d in data]
    zero_pos = 0
    for i, result in enumerate(results):
        if result == 0:
            zero_pos = i
            break
    print(results, zero_pos)
    return results[(zero_pos + 1000) % width] + results[(zero_pos + 2000) % width] + results[(zero_pos + 3000) % width]





if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))

'''
01234
13321

13231

1 -> 0 + 1 = 1
3 -> 0 + 3 = 3
2 -> 1 + 2 = 3
'''

