import re


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


def parse_lines(lines):
    sensors = []
    beacons = set()
    x_min = float('inf')
    x_max = float('inf') * -1
    for line in lines:
        stripped = re.sub(r'[^0-9,:-]', '', line)
        sensor, beacon = stripped.split(':')
        sensor_x, sensor_y = map(int, sensor.split(','))
        beacon_x, beacon_y = map(int, beacon.split(','))
        new_sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(new_sensor)
        x_max = max(x_max, new_sensor.sx + new_sensor.distance, beacon_x)
        x_min = min(x_min, new_sensor.sx - new_sensor.distance, beacon_x)
        beacons.add((beacon_x, beacon_y))
    print(x_min, x_max)
    return sensors, beacons, x_min, x_max


def solve(sensors, beacons, x_min, x_max):
    Y_TARGET = 2000000

    possible = 0
    for x in range(x_min, x_max + 1):
        possible += any(manhattan((x, Y_TARGET), (sensor.sx, sensor.sy))
                        <= sensor.distance for sensor in sensors) and (x, Y_TARGET) not in beacons
    return possible


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(*parsed_lines))
