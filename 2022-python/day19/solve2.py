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

    can_build_geode_robot = ore >= bp4 and obs >= bp5
    can_build_obsidian_robot = ore >= bp2 and cla >= bp3
    can_build_ore_botot = ore >= bp0
    can_build_clay_robot = ore >= bp1

    missing_ore = bp4 - ore
    missing_obs = bp5 - obs

    minutes_needed_for_1_extra_geode = 2
    if minute < minutes_needed_for_1_extra_geode: return finish(minute, geo, geo_bot)
    if can_build_geode_robot: return build_geo_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
    
    minutes_needed_for_1_extra_geode = 3
    if minute < minutes_needed_for_1_extra_geode: return finish(minute, geo, geo_bot)

    if missing_obs > 0 and obs_bot == 0:
        minutes_needed_for_1_extra_geode = 4
        if minute < minutes_needed_for_1_extra_geode: return finish(minute, geo, geo_bot)
        if can_build_obsidian_robot: return build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)
    
    minutes_needed_for_ore = missing_ore / ore_bot
    if minutes_needed_for_ore > 1:
        minutes_needed_for_1_extra_geode = 4
        if minute < minutes_needed_for_1_extra_geode: return finish(minute, geo, geo_bot)
        
    # Catch all
    if missing_obs > 0 and obs_bot == 0 and can_build_obsidian_robot:
        dcs += build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    obs_bot_still_useful = minute > 3
    if can_build_obsidian_robot and obs_bot_still_useful:
        dcs += build_obs_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    cla_needed = cla - bp3
    cla_bot_still_useful = minute > 5 and minute > 5 + cla_needed
    if can_build_clay_robot and cla_bot_still_useful:
        dcs += build_clay_bot(dcs, bp, minute, memo, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, geo_bot)

    if can_build_ore_botot and minute > 5:
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