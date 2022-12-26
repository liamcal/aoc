ans = 0
with open('in.txt') as f:
    for line in f: 
        a, b = (r.split('-') for r in line.strip().split(','))
        range_a = set(range(int(a[0]), int(a[1])+1))
        range_b = set(range(int(b[0]), int(b[1])+1))
        # print(range_a, range_b)
        if len(range_a - range_b) == 0 or len(range_b - range_a) == 0:
            print('found one', a, b)
            ans += 1
print(ans)