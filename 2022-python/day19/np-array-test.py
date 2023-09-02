import re
import time
import numpy as np

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
BLUEPRINTS = [string_to_numbers(line)[1:] for line in lines]
COSTS = [np.array(l) for l in [[[bp[0], 0, 0, 0],[bp[1], 0, 0, 0],[bp[2], bp[3], 0, 0],[bp[4], 0, bp[5], 0]] for bp in BLUEPRINTS]]
NEW_BOTS = [np.array(l) for l in [[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]]

def solve(minute, max_geodes, resources, bots, bp_index, max_minutes, run):
    # Calculate max geodes possible
    minutes_left = max_minutes - minute
    current_geo = resources[3]
    current_geo_bots_can_still_produce = bots[3] * minutes_left
    new_geo_bots_can_still_produce = minutes_left * (minutes_left - 1) / 2
    max_geodes_possible = current_geo + current_geo_bots_can_still_produce + new_geo_bots_can_still_produce
    # print(max_geodes_possible)
    if max_geodes_possible <= max_geodes:
        return max_geodes, run
    if run > 100000:
        return max_geodes, run
    
    print(minute, bots, resources, max_geodes_possible, max_geodes, run)
        
    if minute == max_minutes:
        return resources[3], run
    
    run += 1
    minute += 1
    minutes_left = max_minutes - minute
    
    ore, cla, obs, geo = resources
    ore_bot, cla_bot, obs_bot, geo_bot = bots

    geo_obs = COSTS[bp_index][3][2]
    obs_ore = COSTS[bp_index][2][0]
    obs_cla = COSTS[bp_index][2][1]

    missing_obs = geo_obs - obs
    can_build_obs_bot = ore >= obs_ore and cla >= obs_cla
    minutes_for_1_extra_geode = 4

    if missing_obs > obs_bot:
        if missing_obs > 1 + obs_bot * 2: minutes_for_1_extra_geode = 5
        if missing_obs > 1 + obs_bot * 4: minutes_for_1_extra_geode = 6
        if missing_obs > 2 + obs_bot * 8: minutes_for_1_extra_geode = 7
        if missing_obs > 2 + obs_bot * 16: minutes_for_1_extra_geode = 8
        if missing_obs > 3 + obs_bot * 32: minutes_for_1_extra_geode = 9
        if minute < minutes_for_1_extra_geode: 
            max_geodes, run = solve(minute, max_geodes, resources + bots, bots, bp_index, max_minutes, run)
        if can_build_obs_bot: 
            max_geodes, run = solve(minute, max_geodes, resources + bots - COSTS[bp_index][2], bots + NEW_BOTS[2], bp_index, max_minutes, run)

    if all(x >= 0 for x in resources - COSTS[bp_index][3]):
        max_geodes, run = solve(minute, max_geodes, resources + bots - COSTS[bp_index][3], bots + NEW_BOTS[3], bp_index, max_minutes, run)
    
    if all(x >= 0 for x in resources - COSTS[bp_index][2]):
        max_geodes, run = solve(minute, max_geodes, resources + bots - COSTS[bp_index][2], bots + NEW_BOTS[2], bp_index, max_minutes, run)
    
    if all(x >= 0 for x in resources - COSTS[bp_index][1]):
        max_geodes, run = solve(minute, max_geodes, resources + bots - COSTS[bp_index][1], bots + NEW_BOTS[1], bp_index, max_minutes, run)
    
    if all(x >= 0 for x in resources - COSTS[bp_index][0]):
        max_geodes, run = solve(minute, max_geodes, resources + bots - COSTS[bp_index][0], bots + NEW_BOTS[0], bp_index, max_minutes, run)

    max_geodes, run = solve(minute, max_geodes, resources + bots, bots, bp_index, max_minutes, run)
    return max_geodes, run

def solve_blueprints(blueprint_count, max_minutes):
    bp_max_geodes = []
    for bp_index in range(blueprint_count):
        minute = 0
        max_geodes = 0
        run = 0
        bots = np.array([1, 0, 0, 0])
        resources = np.array([0, 0, 0, 0])
        start = time.perf_counter()
        max_geodes, run = solve(minute, max_geodes, resources, bots, bp_index, max_minutes, run)
        bp_max_geodes.append(max_geodes)
        delta = (time.perf_counter() - start) * 1000
        print(bp_index, BLUEPRINTS[bp_index], bp_max_geodes[-1], f'{delta:.4f} ms')
    return bp_max_geodes

# Part 1
print("*** Part 1 ***")
bp_max_geodes = solve_blueprints(len(BLUEPRINTS), 24)
score_part1 = sum([(bp_index + 1) * max_g for bp_index, max_g in enumerate(bp_max_geodes)])
print("Max geodes:", bp_max_geodes)
print("Score part 1:", score_part1)