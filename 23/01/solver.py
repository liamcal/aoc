import re


def parse(raw_data):
    return [line.strip() for line in raw_data.split('\n')]


def solve1(data):
    count = 0
    for line in data:
        line_digits = re.sub("[^0-9]", "", line)
        count += int(f'{line_digits[0]}{line_digits[-1]}')

    return count


def solve2(data):
    mapping = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
               'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'zero': '0'}
    words = mapping.keys()
    count = 0
    for line in data:
        digits = []
        for i in range(len(line)):
            if line[i].isdigit():
                digits.append(line[i])
            else:
                for word in words:
                    if line[i:].startswith(word):
                        digits.append(mapping[word])
                        break

        new_count = int(f'{digits[0]}{digits[-1]}')
        count += new_count

    return count


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
