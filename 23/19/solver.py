class ConditionRule:
    def __init__(self, prop, op, threshold, dest_workflow):
        self.prop = prop
        self.prop_value = 'xmas'.find(prop)
        self.op = op
        self.threshold = int(threshold)
        self.dest_workflow = dest_workflow

    def get_next_workflow(self, part):
        if self.op == '>':
            return self.dest_workflow if part[self.prop] > self.threshold else None
        elif self.op == '<':
            return self.dest_workflow if part[self.prop] < self.threshold else None

    def split_range(self, range):
        property_range = get_property_range(self.prop, range)
        if self.op == '>':
            if property_range[0] > self.threshold:
                # everything satisfies
                return range, None
            elif property_range[1] <= self.threshold:
                # nothing satisfies
                return None, range
            satisfies = tuple([r if i != self.prop_value else (
                self.threshold + 1, r[1]) for i, r in enumerate(range)])
            remaining = tuple([r if i != self.prop_value else (
                r[0], self.threshold) for i, r in enumerate(range)])
            return satisfies, remaining
        elif self.op == '<':
            if property_range[1] < self.threshold:
                # everything satisfies
                return range, None
            elif property_range[0] >= self.threshold:
                # nothing satisfies
                return None, range
            satisfies = tuple(((r if i != self.prop_value else (
                r[0], self.threshold - 1))for i, r in enumerate(range)))
            remaining = tuple((r if i != self.prop_value else (
                self.threshold, r[1]) for i, r in enumerate(range)))
            return satisfies, remaining

    def __repr__(self):
        return f'CR {self.prop} {self.op} {self.threshold} {self.dest_workflow}'


class FallbackRule:
    def __init__(self, dest_workflow):
        self.dest_workflow = dest_workflow

    def get_next_workflow(self, part):
        return self.dest_workflow

    def split_range(self, range):
        return range, None

    def __repr__(self):
        return f'FR {self.dest_workflow}'


class Workflow:
    def __init__(self, label, rules):
        self.label = label
        self.rules = parse_rules(rules)

    def get_next_workflow(self, part):
        for rule in self.rules:
            rule_result = rule.get_next_workflow(part)
            if rule_result is not None:
                return rule_result

    def get_next_workflows_for_range(self, range):
        range_destinations = {}
        cur_range = range
        for rule in self.rules:
            satisfies, remaining = rule.split_range(cur_range)
            if satisfies is not None:
                range_destinations[satisfies] = rule.dest_workflow
            if remaining is None:
                return range_destinations
            cur_range = remaining

    def __repr__(self):
        return f'W:{self.label} - {self.rules}'


def parse_rules(rules):
    parsed = []
    for rule in rules:
        rule_parts = rule.split(':')
        if len(rule_parts) == 1:
            parsed.append(FallbackRule(rule_parts[0]))
        else:
            rest, dest_workflow = rule_parts
            op = '>' if '>' in rest else '<'
            prop, threshold = rest.split(op)
            parsed.append(ConditionRule(prop, op, threshold, dest_workflow))
    return parsed


def parse(raw_data):
    r_workflows, r_parts = raw_data.split('\n\n')
    r_workflows = r_workflows.split('\n')
    r_parts = r_parts.split('\n')
    parts = []
    workflows = {}
    for line in r_workflows:
        label, rules = line.split('{')
        rules = rules[:-1].split(',')
        workflows[label] = Workflow(label, rules)

    for line in r_parts:
        components = line[1:-1].split(',')
        part = {}
        for component in components:
            k, v = component.split('=')
            part[k] = int(v)
        parts.append(part)
    return workflows, parts


def solve1(data):
    workflows, parts = data
    ans = 0
    for part in parts:
        cur_workflow_label = 'in'
        while cur_workflow_label not in ['A', 'R']:
            cur_workflow = workflows[cur_workflow_label]
            cur_workflow_label = cur_workflow.get_next_workflow(part)
        if cur_workflow_label == 'A':
            ans += sum(v for v in part.values())
    return ans


def score_range(range):
    score = 1
    for r in range:
        score *= r[1] - r[0] + 1
    return score


def get_property_range(s, range):
    return range['xmas'.index(s)]


def solve2(data):
    workflows, _ = data
    ans = 0
    ranges = {((1, 4000),  (1, 4000),  (1, 4000), (1, 4000)): 'in'}
    while ranges:
        new_ranges = {}
        for cur_range, range_name in ranges.items():
            if range_name == 'R':
                continue
            if range_name == 'A':
                ans += score_range(cur_range)
            else:
                next_ranges = workflows[range_name].get_next_workflows_for_range(
                    cur_range)

                new_ranges.update(next_ranges)
        ranges = new_ranges
    return ans


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
