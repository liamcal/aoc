import re
import pickle

from z3 import Int, Solver, If


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        self.distance = self.calc_distance()
        self.circumference_points = self.calc_circ()

    def calc_distance(self):
        return manhattan((self.sx, self.sy), (self.bx, self.by))

    def calc_circ(self):
        circ = []
        for y in range(0, self.distance + 1):
            x = self.distance - y
            circ.append((x, y))
            if y != 0:
                circ.append((x, y*-1))
            if x != 0:
                circ.append((-1*x, y,))
            if y != 0 and x != 0:
                circ.append((-1*x, -1*y))
        return circ

    def __repr__(self):
        return f'<Sensor: ({self.sx}, {self.sy}) -> Beacon: ({self.bx}, {self.by}), Dist: {self.distance}>'


global XY_MAX
XY_MAX = 4000000

global SAVE, LOAD
SAVE = False
LOAD = True
def parse_lines(lines):
    if (LOAD):
        with open('sensors.dump', 'rb') as f:
            return pickle.load(f)
    sensors = []
    beacons = set()
    circ_points = set()
    x_min = float('inf')
    x_max = float('inf') * -1
    for line in lines:
        stripped = re.sub(r'[^0-9,:-]', '', line)
        sensor, beacon = stripped.split(':')
        sensor_x, sensor_y = map(int, sensor.split(','))
        beacon_x, beacon_y = map(int, beacon.split(','))
        new_sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(new_sensor)
        for p in new_sensor.circumference_points:
            if p[0] >= 0 and p[0] <= XY_MAX and p[1] >= 0 and p[1] <= XY_MAX:
                circ_points.add(p)
        x_max = max(x_max, new_sensor.sx + new_sensor.distance, beacon_x)
        x_min = min(x_min, new_sensor.sx - new_sensor.distance, beacon_x)
        beacons.add((beacon_x, beacon_y))
    print(x_min, x_max)
    if(SAVE):
        with open('sensors.dump', 'wb') as f:
            pickle.dump((sensors, beacons, circ_points), f)
            print("dumped")
    return sensors, beacons, circ_points


def solve(sensors, beacons, circ_points):
    print(len(sensors))
    targets = [(-1, -1),(1, -1),(-1, 1),(1, 1)]
    for i, cp in enumerate(circ_points):
        if i % 100_000 == 0: 
            print(i)
        x, y = cp
        for xd, yd in targets:
            target = x + xd, y + yd
            opposite = x + xd * 2, y + yd * 2
            if opposite in circ_points and target not in circ_points:
                print("Found")
                print(cp, target, opposite)

if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(*parsed_lines))
    # print(solve(None, None, None, None))

"""
PP.p..
P..p..
...p..
...p..
...p..

"""