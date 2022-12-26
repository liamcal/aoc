### did this with dijkstra, but BFS may have been sufficient

from queue import PriorityQueue

class Position():
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.neighbors = []
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def can_move(self, other):
        return other.n <= self.n + 1
    
    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def print_neighbor_list(self):
        return ', '.join(f'({neighbor.x}, {neighbor.y})' for neighbor in self.neighbors)
    def __repr__(self):
        return f'<(x: {self.x}, y: {self.y}), n: {self.n}, neighbors: {self.print_neighbor_list()}>'

def read_file(filename = 'in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return [
            [Position(x, y, ord(value)) for x, value in enumerate(list(line))] 
        for y, line in enumerate(lines)]
    

def djikstra(grid, start):
    D = [[float('inf') for _ in range(len(grid[0]))] for __ in range(len(grid))]
    D[start.y][start.x] = 0

    visited = set()
    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        dist, current_position = pq.get()
        visited.add((current_position.x, current_position.y))
        for neighbor in current_position.neighbors:
            if (neighbor.x, neighbor.y) not in visited:
                old_cost = D[neighbor.y][neighbor.x]
                new_cost = D[current_position.y][current_position.x] + 1
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor.y][neighbor.x] = new_cost
    for y, line in enumerate(D):
        print([(chr(grid[y][x].n), cost) for x, cost in enumerate(line)])
    return D



def solve(parsed_lines, start, end):
    grid = parsed_lines
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    start = grid[start[0]][start[1]]
    target = grid[end[0]][end[1]]
    for y, row in enumerate(grid):
        for x, current in enumerate(row):
            if x - 1 >= 0:
                left = grid[y][x-1]
                if current.can_move(left):
                    current.add_neighbor(left)
            if x + 1 < WIDTH:
                right = grid[y][x+1]
                if current.can_move(right):
                    current.add_neighbor(right)
            if y - 1 >= 0:
                up = grid[y-1][x]
                if current.can_move(up):
                    current.add_neighbor(up)
            if y + 1 < HEIGHT:
                down = grid[y+1][x]
                if current.can_move(down):
                    current.add_neighbor(down)

    paths = djikstra(grid, start)
    return paths[target.y][target.x]

if __name__ == '__main__':
    start = 20, 0
    end = 20, 58    
    # start = 0, 0 
    # end = 2, 5

    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines, start,end))
