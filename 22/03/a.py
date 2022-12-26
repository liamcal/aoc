def getPriority(s):
    s2 = str(s).lower()
    a = ord('a')
    p = ord(s2) - a + 1
    if (s.isupper()):
        p = p + 26
    return p

ans = 0
with open('in.txt') as f:
    for line in f:
        line = line.strip()
        midpoint = int(len(line) / 2)
        a, b = set(line[:midpoint]), set(line[midpoint:])
        intersect = a.intersection(b)
        if len(intersect) != 1:
            raise ValueError("Oh no", line)
        common = list(intersect)[0]
        p = getPriority(common)
        ans += p
        print(common, p, line, a, b)
print(ans)