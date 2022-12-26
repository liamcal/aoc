class Directory:
    def __init__(self, name):
        self.name = name
        self.sub_directories = []
        self.files = []
        self.parent = None
        self.size = None

    def add_file(self, file):
        self.files.append(file)

    def add_sub_dir(self, sub_dir):
        self.sub_directories.append(sub_dir)
        sub_dir.parent = self

    def get_size(self):
        if self.size is None:
            f_sum = sum(f.size for f in self.files)
            self.size = sum(d.get_size() for d in self.sub_directories) + f_sum
        return self.size

    def get_path(self):
        path = self.name
        if self.parent is not None:
            path = self.parent.get_path() + '/' + path


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return lines


def solve(parsed_lines):
    root = Directory('/')
    current_dir = root

    for line in parsed_lines:
        if line.startswith('$ cd'):
            _, __, p = line.split()
            if p == '..':
                current_dir = current_dir.parent
            else:
                target_dirs = [
                    sd for sd in current_dir.sub_directories if sd.name == p]
                if len(target_dirs) != 1:
                    raise ValueError("Could not find directory", line)
                target_dir = target_dirs[0]
                current_dir = target_dir
        elif line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            _, d_name = line.split()
            new_dir = Directory(d_name)
            current_dir.add_sub_dir(new_dir)
        else:
            size, f_name = line.split()
            size = int(size)
            new_file = File(f_name, size)
            current_dir.add_file(new_file)

    n_max = 100000
    ans = 0
    todo = [root]
    while todo:
        current = todo.pop(0)
        size = current.get_size()
        if size <= n_max:
            ans += size
        for d in current.sub_directories:
            todo.append(d)
    return ans


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
