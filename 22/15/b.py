import re

from z3 import Int, Solver, If


def abs_z3(x):
    return If(x >= 0, x, -x)


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

    def calc_distance(self):
        return manhattan((self.sx, self.sy), (self.bx, self.by))

    def __repr__(self):
        return f'<Sensor: ({self.sx}, {self.sy}) -> Beacon: ({self.bx}, {self.by}), Dist: {self.distance}>'


global XY_MAX
XY_MAX = 4000000


def parse_lines(lines):
    sensors = []
    for line in lines:
        stripped = re.sub(r'[^0-9,:-]', '', line)
        sensor, beacon = stripped.split(':')
        sensor_x, sensor_y = map(int, sensor.split(','))
        beacon_x, beacon_y = map(int, beacon.split(','))
        new_sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(new_sensor)
    return sensors


def solve(sensors):
    distress_x = Int('x')
    distress_y = Int('y')

    upper = 4000000
    s = Solver()
    s.add(0 <= distress_x)
    s.add(distress_x <= upper)
    s.add(0 <= distress_y)
    s.add(distress_y <= upper)
    solution = Int('solution')
    s.add(solution == distress_x * 4000000 + distress_y)

    for sensor in sensors:
        s.add(sensor.distance < abs_z3(sensor.sx - distress_x) +
              abs_z3(sensor.sy - distress_y))

    # print('solver', s)
    s.check()
    m = s.model()
    # print('model', m)
    return m


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
    # print(solve(None, None, None, None))
