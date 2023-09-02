import re
import time
import numpy as np
from collections import defaultdict

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
BLUEPRINTS = [string_to_numbers(line)[1:] for line in lines]
COSTS = [np.array(l) for l in [[[bp[0], 0, 0, 0],[bp[1], 0, 0, 0],[bp[2], bp[3], 0, 0],[bp[4], 0, bp[5], 0]] for bp in BLUEPRINTS]]

def calculate_geo_at_end(bots_to_build, bp_index, max_minutes):
    # print('To build:', bots_to_build)
    resources = np.array([0, 0, 0, 0])
    build_bots = [0]
    minute = 0
    for bot in bots_to_build:
        while minute < max_minutes:
            # print('Min', minute, 'Res', resources, 'Build', build_bots)
            enough_resources_to_build_bot = all(r >= 0 for r in resources - COSTS[bp_index][bot])
            if enough_resources_to_build_bot:
                minute += 1
                build_bot_counts = np.array([build_bots.count(bot_index) for bot_index in [0, 1, 2, 3]])
                resources += build_bot_counts
                build_bots.append(bot)
                resources -= COSTS[bp_index][bot]
                # print('Min', minute, 'Building', bot)
                break
            else:
                minute += 1
                build_bot_counts = np.array([build_bots.count(bot_index) for bot_index in [0, 1, 2, 3]])
                resources += build_bot_counts

    while minute < max_minutes:
        # print('Min', minute, 'Res', resources, 'Build', build_bots)
        minute += 1
        build_bot_counts = np.array([build_bots.count(bot_index) for bot_index in [0, 1, 2, 3]])
        resources += build_bot_counts

    # print('Min', minute, 'Res', resources, 'Build', build_bots)

    return resources[3]

def items_with_min_value(d):
    min_value = min(d.values())
    return [(k, v) for k, v in d.items() if v == min_value]

def items_with_max_value(d):
    max_value = max(d.values())
    return [(k, v) for k, v in d.items() if v == max_value]

def go_go(bots_to_build, bp_index, max_minutes):
    # print('To build:', bots_to_build)
    resources = np.array([0, 0, 0, 0])
    build_bots = [0]
    minute = 0
    for bot in bots_to_build:
        while minute < max_minutes:
            # print('Min', minute, 'Res', resources, 'Build', build_bots)
            enough_resources_to_build_bot = all(r >= 0 for r in resources - COSTS[bp_index][bot])
            if enough_resources_to_build_bot:
                minute += 1
                build_bot_counts = np.array([build_bots.count(bot_index) for bot_index in [0, 1, 2, 3]])
                resources += build_bot_counts
                build_bots.append(bot)
                resources -= COSTS[bp_index][bot]
                # print('Min', minute, 'Building', bot)
                break
            else:
                minute += 1
                build_bot_counts = np.array([build_bots.count(bot_index) for bot_index in [0, 1, 2, 3]])
                resources += build_bot_counts

    # print('Min', minute, 'Res', resources, 'Build', build_bots)
    return minute

def fastest_ways_to_next_geo_bot(bots_build, minute, bp_index, max_minutes):
    build_orders = []

    for depth in range(0,7):
        build_orders_for_depth = [[3]]

        for i in range(0,depth):
            new_build_orders_for_depth = []
            for build_order in build_orders_for_depth:
                new_build_orders_for_depth.append([0] + build_order)
                new_build_orders_for_depth.append([1] + build_order)
                new_build_orders_for_depth.append([2] + build_order)
            build_orders_for_depth = new_build_orders_for_depth

        build_orders += build_orders_for_depth
    
    for i, build_order in enumerate(build_orders):
        build_orders[i] = bots_build + build_order
        print(build_order)
    print('Build order count', len(build_orders))
    
    # Calculate the minute at which the geo bot is built
    minute_at_next_geo_bot_per_build_order = defaultdict(int)
    for build_order in build_orders:
        minute = go_go(build_order, bp_index, max_minutes)
        print(build_order, minute)
        if minute < max_minutes:
            minute_at_next_geo_bot_per_build_order[tuple(build_order)] = minute
    print(minute_at_next_geo_bot_per_build_order)
    return minute_at_next_geo_bot_per_build_order

    # Select the fastest build orders
    fastest_build_orders_and_minutes = items_with_min_value(minute_at_next_geo_bot_per_build_order)
    return fastest_build_orders_and_minutes

def solve_blueprint(bp_index, max_minutes):
    print('Costs:')
    for i, cost in enumerate(COSTS[bp_index]): print(i, cost)

    bots_to_build = [1,1,1,2,1,2,3,3]
    geo_at_end = calculate_geo_at_end(bots_to_build, bp_index, max_minutes)
    print ('Geo at end', geo_at_end)
    # exit()

    bots_build = []
    minute = 0
    fastest_build_orders_and_minutes = fastest_ways_to_next_geo_bot(bots_build, minute, bp_index, max_minutes)
    print(fastest_build_orders_and_minutes)

    # Calculate the geo's at end
    geo_at_ends = defaultdict(int)
    for bots_build, minute in fastest_build_orders_and_minutes.items():
        geo_at_end = calculate_geo_at_end(bots_build, bp_index, max_minutes)
        geo_at_ends[tuple(bots_build)] = geo_at_end
        print(bots_build, geo_at_end)
    # best_fastest_build_orders_and_minutes = items_with_max_value(geo_at_ends)
    # print('.')
    # print(best_fastest_build_orders_and_minutes)
    # print('.')

    print(geo_at_ends)
    new_fastest_build_orders_and_minutes2 = []
    for bots_build, minute in geo_at_ends.items():
        print('Bots build', bots_build, 'at minute', minute)
        new_fastest_build_orders_and_minutes = fastest_ways_to_next_geo_bot(list(bots_build), minute, bp_index, max_minutes)    
        print(new_fastest_build_orders_and_minutes)
        new_fastest_build_orders_and_minutes2 += new_fastest_build_orders_and_minutes
    print(new_fastest_build_orders_and_minutes2)

    # Calculate the geo's at end
    geo_at_ends = defaultdict(int)
    for bots_build in new_fastest_build_orders_and_minutes2:
        geo_at_end = calculate_geo_at_end(bots_build, bp_index, max_minutes)
        geo_at_ends[tuple(bots_build)] = geo_at_end
        print(bots_build, geo_at_end)
    best_fastest_build_orders_and_minutes = items_with_max_value(geo_at_ends)
    # exit()

    max_geo_at_end = max(geo_at_ends.values())
    return max_geo_at_end

def solve_blueprints(blueprint_count, max_minutes):
    max_geodes_per_bp = []
    for bp_index in range(0, blueprint_count - 1):
        start = time.perf_counter()
        max_geodes = solve_blueprint(bp_index, max_minutes)
        max_geodes_per_bp.append(max_geodes)
        delta = (time.perf_counter() - start) * 1000
        print(bp_index, BLUEPRINTS[bp_index], max_geodes_per_bp[-1], f'{delta:.4f} ms')
    return max_geodes_per_bp

# Part 1
print("*** Part 1 ***")
max_geodes_per_bp = solve_blueprints(len(BLUEPRINTS), 24)
score_part1 = sum([(bp_index + 1) * max_geodes for bp_index, max_geodes in enumerate(max_geodes_per_bp)])
print("Max geodes:", max_geodes_per_bp)
print("Score part 1:", score_part1)
