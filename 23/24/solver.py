from itertools import combinations
import numpy as np
import sympy
from z3 import Int, Solver, simplify


class Hailstone:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.pos = (x, y, z)
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.delta = (dx, dy, dz)

    def __repr__(self):
        return f'<{(self.x, self.y)}>'

    def intersect(self, other):
        try:
            t1, t2 = np.linalg.solve(
                [[self.dx, -other.dx], [self.dy, -other.dy]], [other.x-self.x, other.y-self.y])
        except np.linalg.LinAlgError:
            pass
        else:
            if t1 < 0 or t2 < 0:
                return None  # in the past
            return (self.x+t1*self.dx, self.y+t1*self.dy)
        return None  # Parallel lines


def parse(raw_data):
    lines = [line.strip() for line in raw_data.split('\n')]
    hailstones = []
    for line in lines:
        pos, delta = line.split(' @ ')
        pos = map(int, pos.split(', '))
        delta = map(int, delta.split(', '))
        hailstones.append(Hailstone(*pos, *delta))

    return hailstones


def solve1(data):
    collisions = []
    lower = 200000000000000
    upper = 400000000000000
    for a, b in combinations(data, 2):
        collision = a.intersect(b)
        if collision is not None and all(lower <= p <= upper for p in collision):
            collisions.append(collision)
    return len(collisions)


def solve_system(data, equations_to_solve):
    positions, velocities, times = sympy.symbols(f'p(:{equations_to_solve})'), sympy.symbols(
        f'v(:{equations_to_solve})'), sympy.symbols(f't(:{equations_to_solve})')
    equations = [
        data[i].pos[j] + times[i] * data[i].delta[j] -
        positions[j] - velocities[j] * times[i]
        for i in range(equations_to_solve) for j in range(3)
    ]
    solution = sympy.solve(equations, *positions, *velocities, *times)[0]
    return sum(solution[:3])


def solve_z3(data, equations_to_solve):
    positions = [Int(f'p_{i}') for i in range(equations_to_solve)]
    velocities = [Int(f'v_{i}') for i in range(equations_to_solve)]
    times = [Int(f't_{i}') for i in range(equations_to_solve)]
    solver = Solver()
    for i in range(equations_to_solve):
        for j in range(3):
            solver.add(data[i].pos[j] + times[i] * data[i].delta[j] ==
                       positions[j] + velocities[j] * times[i])
    solver.check()
    model = solver.model()
    model_positions = [p for p in model.decls() if str(p).startswith('p')]
    return simplify(sum(model[p] for p in model_positions))


def solve2(data):
    # this can be reduced to 3 as any extras is an overdefined system and just slows down calculation
    equations_to_solve = 3
    return solve_system(data, equations_to_solve)
    # return solve_z3(data, equations_to_solve)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
