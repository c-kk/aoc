import re
import time
import math
from collections import defaultdict

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
blueprints = [tuple(string_to_numbers(line)[1:]) for line in lines]

def build_geo_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs.append(do_minute(bp, minute - 1, memo, 
        ore + ore_bot - bp[4], cla + cla_bot, obs + obs_bot - bp[5], geo + geo_bot, 
        ore_bot, cla_bot, obs_bot, geo_bot + 1))
    return dcs

def build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs.append(do_minute(bp, minute - 1, memo, 
        ore + ore_bot - bp[2], cla + cla_bot - bp[3], obs + obs_bot, geo + geo_bot, 
        ore_bot, cla_bot, obs_bot + 1, geo_bot))
    return dcs

def build_ore_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs.append(do_minute(bp, minute - 1, memo,
        ore + ore_bot - bp[0], cla + cla_bot, obs + obs_bot, geo + geo_bot, 
        ore_bot + 1, cla_bot, obs_bot, geo_bot))
    return dcs

def build_clay_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs.append(do_minute(bp, minute - 1, memo, 
        ore + ore_bot - bp[1], cla + cla_bot, obs + obs_bot, geo + geo_bot, 
        ore_bot, cla_bot + 1, obs_bot, geo_bot))
    return dcs

def do_nothing(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs.append(do_minute(bp, minute - 1, memo, 
        ore + ore_bot, cla + cla_bot, obs + obs_bot, geo + geo_bot, 
        ore_bot, cla_bot, obs_bot, geo_bot))
    return dcs

def finish(minute, geo, geo_bot):
    return [geo + minute * geo_bot]

def select_decisions(bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    dcs = []
    bp0, bp1, bp2, bp3, bp4, bp5 = bp

    can_build_geo_bot = ore >= bp4 and obs >= bp5
    can_build_obs_bot = ore >= bp2 and cla >= bp3
    can_build_ore_bot = ore >= bp0
    can_build_cla_bot = ore >= bp1

    missing_ore = bp4 - ore
    missing_obs = bp5 - obs

    minutes_for_1_extra_geode = 2
    if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
    if can_build_geo_bot: return build_geo_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
    
    minutes_for_1_extra_geode = 3
    if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)

    if missing_obs > obs_bot:
        minutes_for_1_extra_geode = 4
        if missing_obs > 1 + obs_bot * 2: minutes_for_1_extra_geode = 5
        if missing_obs > 1 + obs_bot * 4: minutes_for_1_extra_geode = 6
        if missing_obs > 2 + obs_bot * 8: minutes_for_1_extra_geode = 7
        if missing_obs > 2 + obs_bot * 16: minutes_for_1_extra_geode = 8
        if missing_obs > 3 + obs_bot * 32: minutes_for_1_extra_geode = 9
        if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
        if can_build_obs_bot: return build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
    
    if missing_ore > ore_bot:
        minutes_for_1_extra_geode = 4
        if missing_ore > 1 + ore_bot * 2: minutes_for_1_extra_geode = 5
        if missing_ore > 1 + ore_bot * 4: minutes_for_1_extra_geode = 6
        if missing_ore > 2 + ore_bot * 8: minutes_for_1_extra_geode = 7
        if missing_ore > 2 + ore_bot * 16: minutes_for_1_extra_geode = 8
        if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
        if can_build_ore_bot: return build_ore_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    # Catch all
    if missing_obs > 0 and obs_bot == 0 and can_build_obs_bot:
        dcs += build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    obs_bot_still_useful = minute > 3
    if can_build_obs_bot and obs_bot_still_useful:
        dcs += build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    cla_needed = cla - bp3
    cla_bot_still_useful = minute > 5 and minute > 5 + cla_needed
    if can_build_cla_bot and cla_bot_still_useful:
        dcs += build_clay_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    if can_build_ore_bot and minute > 5:
        dcs += build_ore_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    dcs += do_nothing(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    return dcs

def do_minute(bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot):
    if minute == 0: return geo
    
    state = (minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
    if state in memo: return memo[state]

    dcs = select_decisions(bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    max_geodes = max(dcs)
    memo[state] = max_geodes
    return max_geodes

def do_blueprints(blueprints, minute_max):
    max_geodes = []
    for bp_index, bp in enumerate(blueprints):
        minute = minute_max
        ore, cla, obs, geo = 0, 0, 0, 0
        ore_bot, cla_bot, obs_bot, geo_bot = 1, 0, 0, 0
        start = time.perf_counter()
        max_geodes.append(do_minute(bp, minute, defaultdict(int), ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot))
        delta = (time.perf_counter() - start) * 1000
        print(bp_index, bp, max_geodes[-1], f'{delta:.4f} ms')
    return max_geodes

# Part 1
print("*** Part 1 ***")
max_geodes = do_blueprints(blueprints, 24)
score_part1 = sum([(bp_index + 1) * max_g for bp_index, max_g in enumerate(max_geodes)])
print("Max geodes:", max_geodes)
print("Score part 1:", score_part1)

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