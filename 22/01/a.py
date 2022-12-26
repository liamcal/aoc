sums = []
cur_sum = 0
largest_sum = -1
largest_pos = -1

with open('in.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if line == '':
            sums.append((cur_sum, len(sums) + 1))
            cur_sum = 0
        else:
            cur_sum += int(line)


print(list(reversed(sorted(sums, key= lambda x: x[0])))[0:3])