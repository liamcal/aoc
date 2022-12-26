class Monkey():
    def __init__(self, items, operation, divisor_test):
        self.items = items
        self.operation = operation
        self.divisor_test = divisor_test
        self._targets = {True: None, False: None}
        self.inspected = 0

    def set_targets(self, true_target, false_target):
        self._targets = {True: true_target, False: false_target}

    def catch(self, item):
        self.items.append(item)

    def operate(self, item):
        self.inspected += 1
        operator, operand = self.operation
        if operator == '*':
            item *= operand
        elif operator == '+':
            item += operand
        elif operator == '^':
            item **= operand
        item //= 3
        return item

    def test(self, item):
        return item % self.divisor_test == 0

    def have_turn(self):
        while self.items:
            current_item = self.items.pop(0)
            operated_item = self.operate(current_item)
            self._targets[self.test(operated_item)].catch(operated_item)


monkeys = [
    Monkey([96, 60, 68, 91, 83, 57, 85], ('*', 2), 17),
    Monkey([75, 78, 68, 81, 73, 99], ('+', 3), 13),
    Monkey([69, 86, 67, 55, 96, 69, 94, 85], ('+', 6), 19),
    Monkey([88, 75, 74, 98, 80], ('+', 5), 7),
    Monkey([82], ('+', 8), 11),
    Monkey([72, 92, 92], ('*', 5), 3),
    Monkey([74, 61], ('^', 2), 2),
    Monkey([76, 86, 83, 55], ('+', 4), 5)]

monkeys[0].set_targets(monkeys[2], monkeys[5])
monkeys[1].set_targets(monkeys[7], monkeys[4])
monkeys[2].set_targets(monkeys[6], monkeys[5])
monkeys[3].set_targets(monkeys[7], monkeys[1])
monkeys[4].set_targets(monkeys[0], monkeys[2])
monkeys[5].set_targets(monkeys[6], monkeys[3])
monkeys[6].set_targets(monkeys[3], monkeys[1])
monkeys[7].set_targets(monkeys[4], monkeys[0])

N_ROUNDS = 20
def solve():
    for _ in range(N_ROUNDS):
        for monkey in monkeys:
            monkey.have_turn()
    for i, monkey in enumerate(monkeys):
        print(i, monkey.inspected)



if __name__ == '__main__':
    solve()