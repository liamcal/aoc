import re
from heapq import heapify, heappop, heappush
import sys
import math 

def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


packet_length = 4

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

names= {ORE: 'ore', CLAY: 'clay', OBSIDIAN: 'obsidian', GEODE: 'geode'}
robots = [ORE, CLAY, OBSIDIAN, GEODE]
resources = robots + []

global TIME_LIMIT
TIME_LIMIT = 24


def parse_lines(lines):
    blueprints = {}
    for line in lines:
        blueprint_number, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian = map(
            int, re.sub(r'[^0-9\s]', '', line).split())
        blueprints[blueprint_number] = {ORE: {ORE: ore_robot_cost_ore}, CLAY: {ORE: clay_robot_cost_ore}, OBSIDIAN: {
            ORE: obsidian_robot_cost_ore, CLAY: obsidian_robot_cost_clay}, GEODE: {ORE: geode_robot_cost_ore, OBSIDIAN: geode_robot_cost_obsidian}}
    return blueprints


def get_time(state):
    return state[0]


def get_resources(state):
    return state[1:5]


def get_resource(state, resource):
    return state[resource + 1]


def get_robots(state):
    return state[5:9]


def get_robot(state, robot):
    return state[robot + 5]


def solve(blueprints):
    ans = 0
    for blueprint_number in blueprints:
        blueprint = blueprints[blueprint_number]
        # (time, [resources], [robots])
        start = (1, 0, 0, 0, 0, 1, 0, 0, 0)
        seen = set()
        max_score = 0
        todo = [start]
        i = 0
        while todo:
            i += 1
            # stack, so pop from end
            current_state = heappop(todo)
            # print("Testing", current_state)
            current_time = get_time(current_state)
            time_remaining = TIME_LIMIT - current_time + 1
            for robot in robots:
                times = [1]
                costs_to_build = blueprint[robot]
                can_build = True
                for resource in costs_to_build:
                    have = get_resource(current_state, resource)
                    need = costs_to_build[resource] - have
                    if need > 0:
                        acquire_rate = get_robot(current_state, resource)
                        # if robot == OBSIDIAN:
                        #     print("Trying to build an obsidian with", names[resource], "Have", have, "Need", need, "Rate", acquire_rate)
                        if acquire_rate > 0:
                            # can build later
                            built_by = math.ceil(need / acquire_rate) + 1
                            times.append(built_by)
                            # if robot == OBSIDIAN: 
                            #     print("Will be functional at", built_by)
                        else:
                            # can't build, give up
                            can_build = False
                            break
                time_to_build = max(times)
                finish_time = current_time + time_to_build

                # if robot == OBSIDIAN:
                #     if can_build:
                #         print("Final ready time", time_to_build)
                #     else:
                #         print("Can't build :(")

                if can_build:
                    # print("Attempt to build bot", names[robot], "Will cost", blueprint[robot])
                    if finish_time > TIME_LIMIT:

                        # we will finish too late, just wait this one out and record our result
                        current_geodes = get_resource(current_state, GEODE)
                        current_rate = get_robot(current_state, GEODE)
                        new_score = current_geodes + time_remaining * current_rate
                        if new_score > max_score:
                            # print("new best", new_score, current_state)
                            # input()
                            max_score = new_score
                        # elif new_score == max_score and new_score > 6:
                        #     print("tie", new_score, current_state)
                        #     input()
                        break

                    current_robots = get_robots(current_state)
                    new_robots = [count + 1 if robot_number == robot else count for robot_number, count in enumerate(current_robots)]

                    new_resources = list(get_resources(current_state))
                    # gather new resources
                    for resource in resources:
                        existing_amount = get_resource(current_state, resource)
                        current_rate = get_robot(current_state, resource)
                        new_amount = existing_amount + current_rate * time_to_build
                        # pay if we need to
                        cost = 0
                        if resource in blueprint[robot]:
                            cost = blueprint[robot][resource]
                            new_amount -= cost
                        # print("Updating", names[resource], "Existing amount", existing_amount, "Existing rate", current_rate, "Build time", time_to_build, "Cost", cost, "New amount", new_amount)
                        new_resources[resource] = new_amount
                    new_state = tuple([finish_time] + new_resources + new_robots)

                    highest_possible_geodes = get_resource(new_state, GEODE)
                    current_geode_robots = get_robot(new_state, GEODE)
                    for i in range(time_remaining):
                        highest_possible_geodes += current_geode_robots
                        current_geode_robots += 1

                    if new_state not in seen:
                        seen.add(new_state)
                        if highest_possible_geodes >= max_score:
                            heappush(todo, new_state)          
                            # building a geode is best, don't try the others
                            if robot == GEODE:
                                # print("Built a geode bot", new_state)
                                break

            # print()
        ans += max_score * blueprint_number
        print("Best for blueprint", blueprint_number, "is", max_score, "Adding", max_score * blueprint_number)
    return ans


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
