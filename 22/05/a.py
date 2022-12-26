strs = ['HBVWNMLP', 'MQH', 'NDBGFQML', 'ZTFQMWG', 'MTHP', 'CBMJDHGT', 'MNBFVR', 'PLHMRGS', 'PDBCN']
stacks = [list(s) for s in strs]

def parse_line(line: str):
    parts = line.strip().split()
    return (int(parts[1]), int(parts[3]), int(parts[5]))

def move(n, start, stop):
    for _ in range(n):
        cur = stacks[start - 1].pop()
        stacks[stop - 1].append(cur)

with open('in.txt') as f:
    for line in f: 
        instructions = parse_line(line)
        move(*instructions)
        # print("Moving", instructions)
        # print(stacks)
print(''.join(stack[-1] for stack in stacks))