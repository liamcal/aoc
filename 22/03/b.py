import itertools
# generator 
def partition(lst, size):
    for i in range(0, len(lst), size):
        yield list(itertools.islice(lst, i, i + size))

# size of each chunk
n = 3

# partition the list

def getPriority(s):
    s2 = str(s).lower()
    a = ord('a')
    p = ord(s2) - a + 1
    if (s.isupper()):
        p = p + 26
    return p

ans = 0
with open('in.txt') as f:
    lines = f.readlines()
    partitioned = partition(lines, n)
    for group in partitioned:
        a,b,c = (s.strip() for s in group)
        intersection = set(a).intersection(set(b)).intersection(set(c))
        print(intersection, group)
        if len(intersection) != 1:
            raise ValueError("Oh no", group)
        common = list(intersection)[0]
        p = getPriority(common)
        ans += p
        # print(common, p, group, a, b)
print(ans)