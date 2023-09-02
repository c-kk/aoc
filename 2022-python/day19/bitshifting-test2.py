import re
import time
import math
import numpy as np
from collections import defaultdict

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

def list_to_int(lst):
    integer = 0
    for i, num in enumerate(reversed(lst)):
        integer += num << (8 * i)
    return integer

def int_to_list(integer):
    lst = []
    for _ in range(4):
        lst.append(integer & 255)
        integer >>= 8
    return list(reversed(lst))

def get_nth_number(integer, n):
    """Retrieve the nth number from the bit-shifted integer."""
    return (integer >> (8 * (3 - n))) & 255


data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
blueprints = [string_to_numbers(line)[1:] for line in lines]

NEW_BOTS = [
    list_to_int([1, 0, 0, 0]),
    list_to_int([0, 1, 0, 0]),
    list_to_int([0, 0, 1, 0]),
    list_to_int([0, 0, 0, 1]),
]

COSTS_LISTS = [[
    [bp[0], 0, 0, 0],
    [bp[1], 0, 0, 0],
    [bp[2], bp[3], 0, 0],
    [bp[4], 0, bp[5], 0],
] for bp in blueprints]

COSTS_INTS = [[
    list_to_int([bp[0], 0, 0, 0]),
    list_to_int([bp[1], 0, 0, 0]),
    list_to_int([bp[2], bp[3], 0, 0]),
    list_to_int([bp[4], 0, bp[5], 0]),
] for bp in blueprints]

def build_ore_bot(minute, memo, resources, bots, bp_index): 
    return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][0], bots + NEW_BOTS[0], bp_index)
def build_cla_bot(minute, memo, resources, bots, bp_index): 
    return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][1], bots + NEW_BOTS[1], bp_index)
def build_obs_bot(minute, memo, resources, bots, bp_index): 
    return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][2], bots + NEW_BOTS[2], bp_index)
def build_geo_bot(minute, memo, resources, bots, bp_index): 
    return do_minute(minute - 1, memo, resources + bots - COSTS_INTS[bp_index][3], bots + NEW_BOTS[3], bp_index)
def do_nothing(minute, memo, resources, bots, bp_index): 
    return do_minute(minute - 1, memo, resources + bots, bots, bp_index)

def finish(minute, geo, geo_bot): return geo + minute * geo_bot

def do_next_action(minute, memo, resources, bots, bp_index):
    geo = get_nth_number(resources, 3)
    geo_bot = get_nth_number(bots, 3)
    if minute == 1: 
        return finish(minute, geo, geo_bot)    

    ore = get_nth_number(resources, 0)
    geo_ore = COSTS_LISTS[bp_index][3][0]
    obs = get_nth_number(resources, 2)
    geo_obs = COSTS_LISTS[bp_index][3][2]
    can_build_geo_bot = ore >= geo_ore and obs >= geo_obs
    if can_build_geo_bot: return build_geo_bot(minute, memo, resources, bots, bp_index)
    if minute == 2: return finish(minute, geo, geo_bot)
    if minute == 3: return do_nothing(minute, memo, resources, bots, bp_index)
    
    minutes_for_1_extra_geode = 4
    
    missing_obs = geo_obs - obs
    obs_bot = get_nth_number(bots, 2)
    cla = get_nth_number(resources, 1)
    obs_ore = COSTS_LISTS[bp_index][2][0]
    obs_cla = COSTS_LISTS[bp_index][2][1]
    can_build_obs_bot = ore >= obs_ore and cla >= obs_cla
        
    if missing_obs > obs_bot:
        if missing_obs > 1 + obs_bot * 2: minutes_for_1_extra_geode = 5
        if missing_obs > 1 + obs_bot * 4: minutes_for_1_extra_geode = 6
        if missing_obs > 2 + obs_bot * 8: minutes_for_1_extra_geode = 7
        if missing_obs > 2 + obs_bot * 16: minutes_for_1_extra_geode = 8
        if missing_obs > 3 + obs_bot * 32: minutes_for_1_extra_geode = 9
        if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
        if can_build_obs_bot: return build_obs_bot(minute, memo, resources, bots, bp_index)
    
    missing_ore = geo_ore - ore
    ore_bot = get_nth_number(bots, 0)

    ore_ore = COSTS_LISTS[bp_index][0][0]
    can_build_ore_bot = ore >= ore_ore
    if missing_ore > ore_bot:
        if missing_ore > 1 + ore_bot * 2: minutes_for_1_extra_geode = 5
        if missing_ore > 1 + ore_bot * 4: minutes_for_1_extra_geode = 6
        if missing_ore > 2 + ore_bot * 8: minutes_for_1_extra_geode = 7
        if missing_ore > 2 + ore_bot * 16: minutes_for_1_extra_geode = 8
        if minute < minutes_for_1_extra_geode: return finish(minute, geo, geo_bot)
        if can_build_ore_bot: return build_ore_bot(minute, memo, resources, bots, bp_index)

    # Catch all
    decisions = []

    if can_build_obs_bot:
        decisions.append(build_obs_bot(minute, memo, resources, bots, bp_index))
    
    cla_extra_stash = cla - obs_cla
    cla_bot_still_useful = minute > 5 and minute > 5 + cla_extra_stash

    cla_ore = COSTS_LISTS[bp_index][1][0]
    can_build_cla_bot = ore >= cla_ore
    if can_build_cla_bot and cla_bot_still_useful:
        decisions.append(build_cla_bot(minute, memo, resources, bots, bp_index))

    if can_build_ore_bot and minute > 5:
        decisions.append(build_ore_bot(minute, memo, resources, bots, bp_index))

    decisions.append(do_nothing(minute, memo, resources, bots, bp_index))

    max_geodes = max(decisions)

    return max_geodes

def do_minute(minute, memo, resources, bots, bp_index):
    if minute == 0: 
        geo = get_nth_number(resources, 3)
        return geo
    
    state = (minute, resources, bots)
    if state in memo: return memo[state]

    max_geodes = do_next_action(minute, memo, resources, bots, bp_index)

    memo[state] = max_geodes
    return max_geodes

def do_blueprints(blueprints, minute_max):
    max_geodes = []
    for bp_index, bp in enumerate(blueprints):
        minute = minute_max

        bots = list_to_int([1, 0, 0, 0])
        resources = list_to_int([0, 0, 0, 0])
        start = time.perf_counter()
        max_geodes.append(do_minute(minute, defaultdict(int), resources, bots, bp_index))
        delta = (time.perf_counter() - start) * 1000
        print(bp_index, bp, max_geodes[-1], f'{delta:.4f} ms')
    return max_geodes

# Part 1
print("*** Part 1 ***")
max_geodes = do_blueprints(blueprints, 24)
score_part1 = sum([(bp_index + 1) * max_g for bp_index, max_g in enumerate(max_geodes)])
print("Max geodes:", max_geodes)
print("Score part 1:", score_part1)
