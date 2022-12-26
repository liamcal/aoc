# a => r, b => p, c => s
lookup1 = {
    'x': {'a': 4, 'b': 1, 'c': 7}, # rock     => dlw
    'y': {'a': 8, 'b': 5, 'c': 2}, # paper,   => wdl
    'z': {'a': 3, 'b': 9, 'c': 6}, # scissor, => lwd
}

# a => r, b => p, c => s
lookup2 = {
    'x': {'a': 3, 'b': 1, 'c': 2}, # lose, => srp
    'y': {'a': 4, 'b': 5, 'c': 6}, # draw, => rps
    'z': {'a': 8, 'b': 9, 'c': 7}, # win,  => psr
}


score = 0
with open('in.txt') as f:
    for line in f.readlines():
        you, me = line.lower().strip().split()
        score += lookup2[me][you]
print(score)