import re
import time
from functools import reduce
from collections import defaultdict
import math

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

def build_next_bot(minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot): 
    global minute_mem, max_geo_found, loop_count
    
    loop_count += 1

    if minute < 1:
        print(minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot)
    
    # print(f'{loop_count}, min{minute}, oreb{ore_bot}, clab{cla_bot}, obsb{obs_bot}, ore{ore}, cla{cla}, obs{obs}, geo{geo}')
    # print(f'{str(minute).rjust(3)} {str(ore_bot).rjust(2)} {cla_bot} {obs_bot} {str(ore).rjust(3)} {str(cla).rjust(2)} {str(obs).rjust(2)} {str(geo).rjust(2)}')

    ## Do a single thing if next action is obvious    
    # Finish when current state was already visited
    state = (minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot)
    if state in minute_mem: return
    minute_mem.add(state)
    
    # Finish when max_geo_possible is less than max_geo_found
    if max_geo_possible(minute, cla, obs, geo, cla_bot, obs_bot) <= max_geo_found: return

    # Build geo_bot now if possible and add geo for the remaining minutes (don't store the amount of geo bots)
    geo_bot_needed = minute >= 2
    geo_bot_possible = ore >= ore_cos3 and obs >= obs_cos
    if geo_bot_needed and geo_bot_possible:
        new_geo = geo + minute - 1 
        max_geo_found = max(new_geo, max_geo_found)
        return build_next_bot(minute - 1, ore + ore_bot - ore_cos3, cla + cla_bot, obs + obs_bot - obs_cos, new_geo, ore_bot, cla_bot, obs_bot)
    
    # Build obs_bot now if needed and possible and no more ore_bots are needed
    obs_bot_needed = obs + obs_bot * (minute - 2) < obs_cos * (minute - 2)
    obs_bot_possible = ore >= ore_cos2 and cla >= cla_cos
    ore_bot_needed = ore + ore_bot * (minute - 11) < max_ore_cos * (minute - 11)
    if obs_bot_needed and obs_bot_possible and not ore_bot_needed: 
        return build_next_bot(minute - 1, ore + ore_bot - ore_cos2, cla + cla_bot - cla_cos, obs + obs_bot, geo, ore_bot, cla_bot, obs_bot + 1)
    
    ## Do multiple things if next action is not obvious
    stack = []

    # Build cla_bot now if needed and possible
    cla_bot_needed = cla + cla_bot * (minute - 5) < cla_cos * (minute - 5)
    cla_bot_possible = ore >= ore_cos1
    if cla_bot_needed and cla_bot_possible and minute > 5 + cla - cla_cos:
        stack.append((minute - 1, ore + ore_bot - ore_cos1, cla + cla_bot, obs + obs_bot, geo, ore_bot, cla_bot + 1, obs_bot))
    
    ## Try building a bot in the future if next action is not obvious
    # Build obs_bot in future if needed and possible
    if obs_bot_needed and cla_bot > 0:
        ore_needed = max(0, ore_cos2 - ore)
        cla_needed = max(0, cla_cos - cla) 
        mn = 1 + max(math.ceil(ore_needed / ore_bot), math.ceil(cla_needed / cla_bot))
        if (minute - mn) >= 2:
            stack.append((minute - mn, ore + mn * ore_bot - ore_cos2, cla + mn * cla_bot - cla_cos, obs + mn * obs_bot, geo, ore_bot, cla_bot, obs_bot + 1))
    
    # Build ore_bot in future if needed and possible
    if ore_bot_needed:
        ore_needed = max(0, ore_cos0 - ore)
        mn = 1 + math.ceil(ore_needed / ore_bot)
        if (minute - mn) >= 15:
            stack.append((minute - mn, ore + mn * ore_bot - ore_cos0, cla + mn * cla_bot, obs + mn * obs_bot, geo, ore_bot + 1, cla_bot, obs_bot))        

    # Build cla_bot in future if needed and possible
    if cla_bot_needed:
        ore_needed = max(0, ore_cos1 - ore)
        mn = 1 + math.ceil(ore_needed / ore_bot)
        if (minute - mn) >= 12:
            stack.append((minute - mn, ore + mn * ore_bot - ore_cos1, cla + mn * cla_bot, obs + mn * obs_bot, geo, ore_bot, cla_bot + 1, obs_bot))

    # Build geo_bot in future if possible
    if obs_bot > 0:
        ore_needed = max(0, ore_cos3 - ore)
        obs_needed = max(0, obs_cos - obs) 
        mn = 1 + max(math.ceil(ore_needed / ore_bot), math.ceil(obs_needed / obs_bot))
        if (minute - mn) >= 1:
            new_geo = geo + minute - mn 
            max_geo_found = max(new_geo, max_geo_found)
            stack.append((minute - mn, ore + (mn * ore_bot) - ore_cos3, cla + (mn * cla_bot), obs + (mn * obs_bot) - obs_cos, new_geo, ore_bot, cla_bot, obs_bot))


    sorted_stack = sorted(stack, key=sort_stack)
    #print(sorted_stack)
    for state in sorted_stack:
        build_next_bot(*state)

def sort_stack(state):
    minute, ore, cla, obs, geo, ore_bot, cla_bot, obs_bot = state
    return geo * 1000 + obs * 100 + cla * 10 + minute

def solve(blueprints, minute):
    global minute_mem, max_geo_possible_mem, max_geo_found, ore_cos0, ore_cos1, ore_cos2, cla_cos, ore_cos3, obs_cos, max_ore_cos
    max_geo_founds = []
    for bp in blueprints:
        minute_mem = set()
        max_geo_possible_mem = defaultdict(int)
        max_geo_found = 0
        ore_cos0, ore_cos1, ore_cos2, cla_cos, ore_cos3, obs_cos = bp
        max_ore_cos = max(ore_cos0, ore_cos1, ore_cos2, ore_cos3)
        build_next_bot(minute, 0, 0, 0, 0, 1, 0, 0)
        max_geo_founds.append(max_geo_found)
        # print(bp, max_geo_found, loop_count)
    return max_geo_founds

runs = 20
start = time.perf_counter()
loop_count = 0
for _ in range(runs):
    max_geo_founds = solve(blueprints_example, 24)
    score_part1_example = sum([(bp_index + 1) * max_geo_found for bp_index, max_geo_found in enumerate(max_geo_founds)])
    max_geo_founds = solve(blueprints_example[0:3], 32)
    score_part2_example = reduce(lambda x, y: x * y, max_geo_founds)

    max_geo_founds = solve(blueprints_puzzle, 24)
    score_part1_puzzle = sum([(bp_index + 1) * max_geo_found for bp_index, max_geo_found in enumerate(max_geo_founds)])
    max_geo_founds = solve(blueprints_puzzle[0:3], 32)
    score_part2_puzzle = reduce(lambda x, y: x * y, max_geo_founds)

print("*** Scores ***")
print("Score part 1 for example:", score_part1_example, "" if score_part1_example == 33 else "X!")
print("Score part 2 for example:", score_part2_example, "" if score_part2_example == 3472 else "X!")
print("Score part 1 for puzzle:", score_part1_puzzle, "" if score_part1_puzzle == 1413 else "X!")
print("Score part 2 for puzzle:", score_part2_puzzle, "" if score_part2_puzzle == 21080 else "X!")

delta = (time.perf_counter() - start) * 1000
bp_count = runs * (len(blueprints_example) + len(blueprints_example[0:3]) + len(blueprints_puzzle) + len(blueprints_puzzle[0:3]))
print(f'{runs} runs, average time per run {(delta/runs):.2f} ms, loops per bp {loop_count/bp_count:.0f}')