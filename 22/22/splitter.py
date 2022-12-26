with open('split.txt') as f:
    a, b = [], []
    for line in f:
        line = line.strip()
        midpoint = len(line) // 2
        first, second = line[:midpoint], line[midpoint:]
        a.append(first)
        b.append(second)

for line in a:
    print(line)

print()
for line in b:
    print(line)
