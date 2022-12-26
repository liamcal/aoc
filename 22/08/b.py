def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    grid = [[int(t) for t in list(l)] for l in lines]
    return grid


def get_scenic_score(forest, row, col):
    forest_height = len(forest)
    forest_width = len(forest[0])
    size = forest[row][col]

    score = 1
    # score left
    left_count = 0
    for i in range(col - 1, -1, -1):
        left_count += 1
        cur = forest[row][i]
        if cur >= size:
            break
    score *= left_count

    # score right
    right_count = 0
    for i in range(col + 1, forest_width):
        right_count += 1
        cur = forest[row][i]
        if cur >= size:
            break
    score *= right_count

    # score up
    up_count = 0
    for i in range(row - 1, -1, -1):
        up_count += 1
        cur = forest[i][col]
        if cur >= size:
            break
    score *= up_count

    # look down
    down_count = 0
    for i in range(row + 1, forest_height):
        down_count += 1
        cur = forest[i][col]
        if cur >= size:
            break
    score *= down_count

    return score


def solve(parsed_lines):
    forest = parsed_lines
    ans = 0
    for row in range(len(forest)):
        for col in range(len(forest[row])):
            ans = max(ans, get_scenic_score(forest, row, col))
    return ans


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
