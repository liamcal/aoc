def read_file(filename = 'in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

packet_length = 4

def parse_lines(lines):
    return lines[0]

def solve(parsed_lines):
    line = parsed_lines
    for i in range(packet_length, len(line)):
        segment = line[i-packet_length: i]
        if len(set(segment)) == packet_length:
            return ("Found solution:", i, segment)

if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
