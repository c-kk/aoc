import re
import time
from functools import reduce
from collections import defaultdict

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

blueprints_example = [tuple(string_to_numbers(line)[1:]) for line in open('data1.txt').read().split('\n')]
blueprints_puzzle = [tuple(string_to_numbers(line)[1:]) for line in open('data2.txt').read().split('\n')]

def max_geo_possible(minute, cla, obs, geo, cla_bot, obs_bot):
    global max_geo_possible_mem
    state = (minute, cla, obs, geo, cla_bot, obs_bot)
    if state in max_geo_possible_mem: return max_geo_possible_mem[state]

    # Calculate the max_geo_possible fast with special rules
    # - Try to produce 1 bot of each type every minute
    # - All ore costs are zero: geo_bot cost only obs, obs_bot cost only cla, cla_bot is free
    # - This is fast because there is only one solution: build a robot if you can
    # - The max_geo_possible >= the geo produced by following the regular rules
    while minute >= 1:
        can_build_obs_bot = cla >= cla_cos
        can_build_geo_bot = obs >= obs_cos

        # Produce
        cla += cla_bot
        obs += obs_bot

        # Build cla bot for free
        cla_bot += 1

        # Build obs bot if possible
        if can_build_obs_bot: 
            cla -= cla_cos
            obs_bot += 1
        
        # Build geo bot if possible
        if can_build_geo_bot: 
            obs -= obs_cos
            geo += minute - 1
        
        minute -= 1
    max_geo_possible_mem[state] = geo
    return geo

def do_minute(minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot, ore_bot_allowed = True, cla_bot_allowed = True): 
    global minute_mem, max_geo_found, loop_count
    
    loop_count += 1

    ## Do a single thing if next action is obvious
    # Finish when current state was already visited
    state = (minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot)
    if state in minute_mem: return
    minute_mem.add(state)

    # Finish in the last minute
    if minute == 1: 
        max_geo_found = max(geo, max_geo_found)
        return
    
    # Finish when max geo possible is less than max geo found
    if max_geo_possible(minute, cla, obs, geo, cla_bot, obs_bot) <= max_geo_found: return

    # Build geo bot if possible and add geo for the remaining minutes (don't store the amount of geo bots)
    if ore >= ore_cos3 and obs >= obs_cos: 
        return do_minute(minute - 1, ore + ore_bot - ore_cos3, cla + cla_bot, obs + obs_bot - obs_cos, geo + minute - 1, ore_bot, cla_bot, obs_bot)
    
    # Build obs bot if needed and possible and no more ore bots are needed
    obs_bot_needed = obs_cos - obs - obs_bot > 0
    can_build_obs_bot = ore >= ore_cos2 and cla >= cla_cos
    if obs_bot_needed and can_build_obs_bot and not ore_bot < max_ore_cos: 
        return do_minute(minute - 1, ore + ore_bot - ore_cos2, cla + cla_bot - cla_cos, obs + obs_bot, geo, ore_bot, cla_bot, obs_bot + 1)
    
    ## Try multiple things if next action is not obvious
    # Build obs bot if maybe needed and possible
    obs_bot_maybe_needed = obs_bot < obs_cos
    if obs_bot_maybe_needed and can_build_obs_bot: 
        do_minute(minute - 1, ore + ore_bot - ore_cos2, cla + cla_bot - cla_cos, obs + obs_bot, geo, ore_bot, cla_bot, obs_bot + 1)
    
    # Build ore bot if maybe needed and possible and allowed
    ore_bot_maybe_needed = ore_bot < max_ore_cos
    can_build_ore_bot = ore >= ore_cos0 
    if ore_bot_maybe_needed and can_build_ore_bot and ore_bot_allowed: 
        do_minute(minute - 1, ore + ore_bot - ore_cos0, cla + cla_bot, obs + obs_bot, geo, ore_bot + 1, cla_bot, obs_bot)
    
    # Build cla bot if maybe needed and possible and allowed
    cla_bot_maybe_needed = minute > 5 + cla - cla_cos and cla_bot < cla_cos
    can_build_cla_bot = ore >= ore_cos1
    if cla_bot_maybe_needed and can_build_cla_bot and cla_bot_allowed: 
        do_minute(minute - 1, ore + ore_bot - ore_cos1, cla + cla_bot, obs + obs_bot, geo, ore_bot, cla_bot + 1, obs_bot)
    
    # Do nothing. Disallow building an ore bot or cla bot in the next minute, if building this bot was possible in this minute. Don't wait for nothing.
    ore_bot_allowed = not can_build_ore_bot
    cla_bot_allowed = not can_build_cla_bot
    do_minute(minute - 1, ore + ore_bot, cla + cla_bot, obs + obs_bot, geo, ore_bot, cla_bot, obs_bot, ore_bot_allowed, cla_bot_allowed)

def solve(blueprints, minute):
    global minute_mem, max_geo_possible_mem, max_geo_found, ore_cos0, ore_cos1, ore_cos2, cla_cos, ore_cos3, obs_cos, max_ore_cos
    max_geo_founds = []
    for bp in blueprints:
        minute_mem = set()
        max_geo_possible_mem = defaultdict(int)
        max_geo_found = 0
        ore_cos0, ore_cos1, ore_cos2, cla_cos, ore_cos3, obs_cos = bp
        max_ore_cos = max(ore_cos0, ore_cos1, ore_cos2, ore_cos3)
        do_minute(minute, 0, 0, 0, 0, 1, 0, 0)
        max_geo_founds.append(max_geo_found)
        # print(bp, max_geo_found)
    return max_geo_founds

runs = 20
loop_count = 0

def run_part1_and_part2(blueprints):
    start = time.perf_counter()
    for _ in range(runs):
        max_geo_founds = solve(blueprints, 24)
        score_part1 = sum([(bp_index + 1) * max_geo_found for bp_index, max_geo_found in enumerate(max_geo_founds)])
        max_geo_founds = solve(blueprints[0:3], 32)
        score_part2 = reduce(lambda x, y: x * y, max_geo_founds)
    time_needed = (time.perf_counter() - start) * 1000 / runs
    return score_part1, score_part2, time_needed

score_part1_example, score_part2_example, time_example = run_part1_and_part2(blueprints_example)
score_part1_puzzle, score_part2_puzzle, time_puzzle = run_part1_and_part2(blueprints_puzzle)

print("*** Scores ***")
print("Score part 1 for example:", score_part1_example, "" if score_part1_example == 33 else "X!")
print("Score part 2 for example:", score_part2_example, "" if score_part2_example == 3472 else "X!")
print("Score part 1 for puzzle:", score_part1_puzzle, "" if score_part1_puzzle == 1413 else "X!")
print("Score part 2 for puzzle:", score_part2_puzzle, "" if score_part2_puzzle == 21080 else "X!")

bp_count = runs * (len(blueprints_example) + len(blueprints_example[0:3]) + len(blueprints_puzzle) + len(blueprints_puzzle[0:3]))
print(f'{runs} runs, loops per bp {loop_count/bp_count:.0f}')
print(f'Time needed for example {time_example:.2f} ms')
print(f'Time needed for puzzle {time_puzzle:.2f} ms')

# *** Scores ***
# Score part 1 for example: 33 
# Score part 2 for example: 3472 
# Score part 1 for puzzle: 1413 
# Score part 2 for puzzle: 21080 
# 20 runs, loops per bp 327
# Time needed for example 12.60 ms
# Time needed for puzzle 8.72 ms