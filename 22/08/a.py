def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    grid = [[int(t) for t in list(l)] for l in lines]
    return grid


def get_is_visible(forest, row, col):
    forest_height = len(forest)
    forest_width = len(forest[0])
    size = forest[row][col]
    # look left
    if all(forest[row][i] < size for i in range(col - 1, -1, -1)):
        return True
    # look right
    if all(forest[row][i] < size for i in range(col + 1, forest_width)):
        return True
    # look up
    if all(forest[i][col] < size for i in range(row - 1, -1, -1)):
        return True
    # look down
    if all(forest[i][col] < size for i in range(row + 1, forest_height)):
        return True
    return False


def solve(parsed_lines):
    forest = parsed_lines
    ans = 0
    for row in range(len(forest)):
        for col in range(len(forest[row])):
            ans += get_is_visible(forest, row, col)
    return ans


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
