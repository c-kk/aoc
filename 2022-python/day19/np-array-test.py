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
    
    # print(minute, bots, resources, max_geodes_possible)
    
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
exit()





# Part 2
print("*** Part 2 ***")
max_geodes = do_blueprints(blueprints[0:3], 32)
score_part2 = math.prod([max_g for max_g in max_geodes])
print("Max geodes:", max_geodes)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)

# Data 1
# *** Part 1 ***
# 0 (4, 2, 3, 14, 2, 7) 9 172.0309 ms
# 1 (2, 3, 3, 8, 3, 12) 12 544.6428 ms
# Max geodes: [9, 12]
# Score part 1: 33
# *** Part 2 ***
# 0 (4, 2, 3, 14, 2, 7) 54 13020.7538 ms
# 1 (2, 3, 3, 8, 3, 12) 62 33200.9352 ms
# Max geodes: [54, 62]
# Score part 2: 3348

# Data 2
# *** Part 1 ***
# 0 (3, 4, 4, 18, 3, 13) 0 60.6036 ms
# 1 (4, 4, 2, 11, 4, 8) 3 22.9160 ms
# 2 (3, 3, 2, 15, 3, 9) 4 144.0688 ms
# 3 (2, 2, 2, 8, 2, 14) 13 710.4953 ms
# 4 (4, 3, 2, 19, 3, 13) 0 19.7352 ms
# 5 (3, 3, 3, 20, 2, 12) 1 72.0230 ms
# 6 (2, 3, 3, 8, 3, 20) 6 363.6755 ms
# 7 (4, 3, 2, 5, 2, 10) 15 99.4987 ms
# 8 (2, 3, 3, 11, 3, 14) 7 412.5673 ms
# 9 (3, 4, 4, 18, 3, 8) 2 46.4358 ms
# 10 (2, 2, 2, 20, 2, 14) 3 380.6262 ms
# 11 (4, 4, 4, 11, 4, 12) 1 14.1772 ms
# 12 (2, 3, 3, 14, 3, 19) 3 250.4988 ms
# 13 (4, 4, 4, 10, 2, 7) 4 24.6405 ms
# 14 (2, 4, 3, 20, 2, 17) 1 100.7719 ms
# 15 (3, 4, 3, 15, 4, 16) 0 40.2148 ms
# 16 (4, 4, 2, 11, 3, 14) 0 12.9042 ms
# 17 (4, 4, 3, 7, 4, 20) 1 16.3332 ms
# 18 (2, 4, 4, 15, 2, 20) 1 116.6002 ms
# 19 (3, 3, 2, 16, 2, 18) 0 72.1619 ms
# 20 (4, 4, 4, 15, 3, 8) 1 11.1116 ms
# 21 (3, 3, 3, 17, 4, 8) 4 126.8895 ms
# 22 (3, 4, 2, 15, 3, 7) 3 69.2877 ms
# 23 (4, 4, 2, 9, 3, 15) 1 16.1109 ms
# 24 (3, 4, 4, 6, 2, 20) 3 80.7384 ms
# 25 (2, 2, 2, 10, 2, 11) 14 760.0123 ms
# 26 (2, 4, 2, 20, 3, 15) 1 102.3005 ms
# 27 (4, 4, 2, 16, 4, 16) 0 10.7625 ms
# 28 (3, 4, 4, 5, 3, 12) 8 141.8862 ms
# 29 (4, 3, 3, 20, 2, 19) 0 18.8084 ms
# Max geodes: [0, 3, 4, 13, 0, 1, 6, 15, 7, 2, 3, 1, 3, 4, 1, 0, 0, 1, 1, 0, 1, 4, 3, 1, 3, 14, 1, 0, 8, 0]
# Score part 1: 1413
# *** Part 2 ***
# 0 (3, 4, 4, 18, 3, 13) 17 8070.0326 ms
# 1 (4, 4, 2, 11, 4, 8) 31 5633.2367 ms
# 2 (3, 3, 2, 15, 3, 9) 40 14525.9288 ms
# Max geodes: [17, 31, 40]
# Score part 2: 21080

# max_geodes = 0
# ore, cla, obs, geo = int_to_list(resources)
# ore_bot, cla_bot, obs_bot, geo_bot = int_to_list(bots)
# for bot_index in range(5):
#     resources, bots = build_bot(bot_index, resources, bots, bp_index)

#     print(minute, max_geodes)
#     minute -= 1
#     if minute == 0: return max_geodes

# print(minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
# exit()

# if minute == 0: 
#     geo = get_nth_number(resources, 3)
#     return geo

# state = (minute, resources, bots)
# if state in memo: return memo[state]

# max_geodes = do_next_action(minute, memo, resources, bots, bp_index)

# memo[state] = max_geodes
# return max_geodes

# def build_bot(bot_index, minute, memo, resources, bots, bp_index):
#     return do_minute(minute - 1, memo, resources + bots - costs[bot_index], bots + NEW_BOTS[bot_index], bp_index)
# def build_ore_bot(minute, memo, resources, bots, bp_index): 
#     return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][0], bots + NEW_BOTS[0], bp_index)
# def build_cla_bot(minute, memo, resources, bots, bp_index): 
#     return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][1], bots + NEW_BOTS[1], bp_index)
# def build_obs_bot(minute, memo, resources, bots, bp_index): 
#     return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][2], bots + NEW_BOTS[2], bp_index)
# def build_geo_bot(minute, memo, resources, bots, bp_index): 
#     return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][3], bots + NEW_BOTS[3], bp_index)
# def do_nothing(minute, memo, resources, bots, bp_index): 
#     return do_minute(minute - 1, memo, resources + bots, bots, bp_index)
# def finish(minute, geo, geo_bot): return geo + minute * geo_bot

# def do_next_action(minute, memo, resources, bots, bp_index):
#     geo = get_nth_number(resources, 3)
#     geo_bot = get_nth_number(bots, 3)
#     if minute == 1: 
#         return finish(minute, geo, geo_bot)    

#     ore = get_nth_number(resources, 0)
#     geo_ore = COSTS_LISTS[bp_index][3][0]
#     obs = get_nth_number(resources, 2)
#     geo_obs = COSTS_LISTS[bp_index][3][2]
#     can_build_geo_bot = ore >= geo_ore and obs >= geo_obs
#     if can_build_geo_bot: return build_geo_bot(minute, memo, resources, bots, bp_index)
#     if minute == 2: return finish(minute, geo, geo_bot)
#     if minute == 3: return do_nothing(minute, memo, resources, bots, bp_index)
    
#     minutes_for_1_extra_geode = 4
    
#     missing_obs = geo_obs - obs
#     obs_bot = get_nth_number(bots, 2)
#     cla = get_nth_number(resources, 1)
#     obs_ore = COSTS_LISTS[bp_index][2][0]
#     obs_cla = COSTS_LISTS[bp_index][2][1]
#     can_build_obs_bot = ore >= obs_ore and cla >= obs_cla
        
#     if missing_obs > obs_bot:
#         if missing_obs > 1 + obs_bot * 2: minutes_for_1_extra_geode = 5
#         if missing_obs > 1 + obs_bot * 4: minutes_for_1_extra_geode = 6
#         if missing_obs > 2 + obs_bot * 8: minutes_for_1_extra_geode = 7
#         if missing_obs > 2 + obs_bot * 16: minutes_for_1_extra_geode = 8
#         if missing_obs > 3 + obs_bot * 32: minutes_for_1_extra_geode = 9
#         if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
#         if can_build_obs_bot: return build_obs_bot(minute, memo, resources, bots, bp_index)
    
#     missing_ore = geo_ore - ore
#     ore_bot = get_nth_number(bots, 0)

#     ore_ore = COSTS_LISTS[bp_index][0][0]
#     can_build_ore_bot = ore >= ore_ore
#     if missing_ore > ore_bot:
#         if missing_ore > 1 + ore_bot * 2: minutes_for_1_extra_geode = 5
#         if missing_ore > 1 + ore_bot * 4: minutes_for_1_extra_geode = 6
#         if missing_ore > 2 + ore_bot * 8: minutes_for_1_extra_geode = 7
#         if missing_ore > 2 + ore_bot * 16: minutes_for_1_extra_geode = 8
#         if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
#         if can_build_ore_bot: return build_ore_bot(minute, memo, resources, bots, bp_index)

#     # Catch all
#     decisions = []

#     if can_build_obs_bot:
#         decisions.append(build_obs_bot(minute, memo, resources, bots, bp_index))
    
#     cla_extra_stash = cla - obs_cla
#     cla_bot_still_useful = minute > 5 and minute > 5 + cla_extra_stash

#     cla_ore = COSTS_LISTS[bp_index][1][0]
#     can_build_cla_bot = ore >= cla_ore
#     if can_build_cla_bot and cla_bot_still_useful:
#         decisions.append(build_cla_bot(minute, memo, resources, bots, bp_index))

#     if can_build_ore_bot and minute > 5:
#         decisions.append(build_ore_bot(minute, memo, resources, bots, bp_index))

#     decisions.append(do_nothing(minute, memo, resources, bots, bp_index))

#     max_geodes = max(decisions)

#     return max_geodes

# def build_bot(bot_index, resources, bots, bp_index):
#     resources = resources + bots - COSTS_INTS[bp_index][0]
#     bots = bots + NEW_BOTS[0]
#     return resources, bots