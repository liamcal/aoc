from collections import defaultdict
from math import lcm


class Broadcaster:
    def __init__(self, children):
        self.label = 'broadcaster'
        self.children = children

    def add_input(self, input_label):
        pass

    def pulse(self, is_high, input_label):
        return [(child, is_high, self.label) for child in self.children]


class FlipFlop:
    def __init__(self, label, children):
        self.label = label
        self.children = children
        self.is_on = False

    def add_input(self, input_label):
        pass

    def pulse(self, is_high, input_label):
        if is_high:
            return []
        self.is_on = not self.is_on
        return [(child, self.is_on, self.label) for child in self.children]


class Conjunction:
    def __init__(self, label, children):
        self.label = label
        self.children = children
        self.memory = {}

    def add_input(self, input_label):
        self.memory[input_label] = False

    def pulse(self, is_high, input_label):
        self.memory[input_label] = is_high
        out_pulse = not all(v for v in self.memory.values())
        return [(child, out_pulse, self.label) for child in self.children]


def create_module(line):
    m_type, m_out = line.split(' -> ')
    children = m_out.split(', ')
    if m_type[0] == '%':
        return FlipFlop(m_type[1:], children)
    elif m_type[0] == '&':
        return Conjunction(m_type[1:], children)
    elif m_type == 'broadcaster':
        return Broadcaster(children)


def run_cycle(module_map, onSignal):
    broadcaster = module_map['broadcaster']
    todo = broadcaster.pulse(False, 'button')
    while todo:
        target_label, pulse_type, input_label = todo.pop(0)
        onSignal(target_label, pulse_type, input_label)
        if target_label not in module_map:
            continue
        target_module = module_map[target_label]
        new_p = target_module.pulse(pulse_type, input_label)
        todo.extend(new_p)


def parse(raw_data):
    lines = [line.strip() for line in raw_data.split('\n')]
    modules = [create_module(line) for line in lines]
    for module in modules:
        for potential_input in modules:
            if module.label in potential_input.children:
                module.add_input(potential_input.label)
    module_map = {m.label: m for m in modules}
    return module_map


def solve1(data):
    module_map = data
    lows, highs = [], []

    def onSignal(target_label, pulse_type, input_label):
        if pulse_type:
            highs.append(input_label)
        else:
            lows.append(input_label)

    for _ in range(1000):
        lows.append('button')
        run_cycle(module_map, onSignal)
    return len(lows) * len(highs)


def solve2(data):
    module_map = data
    cycles = []
    answers = defaultdict(list)
    targets = set(['xc', 'ct', 'kp', 'ks'])  # manual inspection
    presses = 0

    def onPress(target_label, pulse_type, input_label):
        if target_label in targets and pulse_type == False:
            answers[target_label].append(presses)
            if len(answers[target_label]) == 2:
                targets.remove(target_label)
                cycle_len = presses - min(answers[target_label])
                cycles.append(cycle_len)
    while targets:
        presses += 1
        run_cycle(module_map, onPress)
    return lcm(*cycles)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
