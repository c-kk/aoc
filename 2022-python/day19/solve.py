import re
import time
from collections import defaultdict

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
blueprints = [tuple(string_to_numbers(line)[1:]) for line in lines]
print("Blueprints:", blueprints)

# Part 1
print("*** Part 1 ***")
def do_minute(bp, minute, memo, ore, cla, obs, geo, ore_rob, cla_rob, obs_rob, geo_rob):
    max_minutes = 24
    if minute > max_minutes:
        return geo

    state = (minute, ore, cla, obs, geo, ore_rob, cla_rob, obs_rob, geo_rob)
    if state in memo:
        return memo[state]

    decisions = []
    bp0, bp1, bp2, bp3, bp4, bp5 = bp
    
    # Build geode robot
    if ore >= bp4 and obs >= bp5:
        decisions.append(do_minute(
            bp, minute + 1, memo, 
            ore + ore_rob - bp4, cla + cla_rob, obs + obs_rob - bp5, geo + geo_rob, 
            ore_rob, cla_rob, obs_rob, geo_rob + 1, 
        ))
    else:        
        # Build obsidian robot
        obs_needed = bp5 - obs
        obs_rob_still_useful = minute <= max_minutes - 3
        if ore >= bp2 and cla >= bp3 and obs_rob_still_useful:
            decisions.append(do_minute(
                bp, minute + 1, memo, 
                ore + ore_rob - bp2, cla + cla_rob - bp3, obs + obs_rob, geo + geo_rob, 
                ore_rob, cla_rob, obs_rob + 1, geo_rob, 
            ))

        # Build ore robot
        if ore >= bp0 and minute <= max_minutes - 5:
            decisions.append(do_minute(
                bp, minute + 1, memo,
                ore + ore_rob - bp0, cla + cla_rob, obs + obs_rob, geo + geo_rob, 
                ore_rob + 1, cla_rob, obs_rob, geo_rob
            ))

        # Build clay robot
        cla_needed = cla - bp3
        cla_rob_still_useful = minute <= max_minutes - 5 and minute <= max_minutes - 5 - cla_needed
        if ore >= bp1 and cla_rob_still_useful:
            decisions.append(do_minute(
                bp, minute + 1, memo, 
                ore + ore_rob - bp1, cla + cla_rob, obs + obs_rob, geo + geo_rob, 
                ore_rob, cla_rob + 1, obs_rob, geo_rob, 
            ))

        # Do nothing
        decisions.append(do_minute(
            bp, minute + 1, memo, 
            ore + ore_rob, cla + cla_rob, obs + obs_rob, geo + geo_rob, 
            ore_rob, cla_rob, obs_rob, geo_rob, 
        ))

    max_geodes = max(decisions)
    memo[state] = max_geodes
    return max_geodes

score_part1 = 0
for bp_index, bp in enumerate(blueprints):
    minute = 1
    memo = defaultdict(int)
    ore = 0
    cla = 0
    obs = 0
    geo = 0
    ore_rob = 1
    cla_rob = 0
    obs_rob = 0
    geo_rob = 0

    start = time.perf_counter()
    max_geodes = do_minute(bp, minute, memo, ore, cla, obs, geo, ore_rob, cla_rob, obs_rob, geo_rob)    
    delta = (time.perf_counter() - start) * 1000
   
    quality_level = (bp_index + 1) * max_geodes
    score_part1 += quality_level

    print(bp_index, bp, max_geodes, quality_level, f'{delta:.4f} ms')
    
print("Score part 1:", score_part1)