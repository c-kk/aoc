from pathfinding import *
from itertools import combinations

# Read the data and build the graph
graph = SimpleGraph()
graph.edges = {}
blocked_valves = []
flowrates = {}

data_version = input("Data version (1 or 2): ")
filename = "data2.txt" if data_version == "2" else "data1.txt"
with open(filename) as file:
    for line in file:
        parts = line.strip().split(";")
        valve_name, flowrate_str = parts[0].split()[1], parts[0].split("=")[1]
        flowrate = int(flowrate_str)
        flowrates[valve_name] = flowrate
        if flowrate > 0:
            blocked_valves.append(valve_name)
        graph.edges[valve_name] = [t.split()[-1] for t in parts[1].split(",")]

# Function to find the distance to target
distance_cache = {}
def distance_to_target(current, target):
    if (current, target) not in distance_cache:
        came_from = breadth_first_search(graph, current, target)
        distance_cache[(current, target)] = len(reconstruct_path(came_from, start=current, goal=target)[1:])
    return distance_cache[(current, target)]

# Recursive function to calculate pressure
def calc_pressure(pressure, minutes_left, current, target, blocked_valves):
    distance = distance_to_target(current, target)
    minutes_left -= distance + 1
    if minutes_left <= 0:
        return pressure
    
    pressure += minutes_left * flowrates[target]
    
    blocked_valves_new = list(blocked_valves)
    blocked_valves_new.remove(target)
    if not blocked_valves_new:
        return pressure

    pressures_next = [calc_pressure(pressure, minutes_left, target, next_target, tuple(blocked_valves_new)) for next_target in blocked_valves_new]
    return max(pressures_next)

# Part 1
max_pressure_part1 = 0
for target in blocked_valves:
    pressure = calc_pressure(0, 30, 'AA', target, tuple(blocked_valves))
    max_pressure_part1 = max(max_pressure_part1, pressure)
    print(f'{target}: {pressure}')

print("Score part 1:", max_pressure_part1)

# Part 2
max_pressure_part2 = 0

# Iterate through combinations of dividing the blocked valves, only up to half the size
half_length = 1 + len(blocked_valves) // 2
for i in range(half_length):
    for blocked_valves_you in combinations(blocked_valves, i):
        blocked_valves_you = list(blocked_valves_you)
        blocked_valves_ele = list(set(blocked_valves) - set(blocked_valves_you))

        max_pressure_you = 0
        for target in blocked_valves_you:
            pressure = calc_pressure(0, 26, 'AA', target, tuple(blocked_valves_you))
            max_pressure_you = max(max_pressure_you, pressure)
            print(f'Y {blocked_valves_you} -> {target}: {pressure}')

        max_pressure_ele = 0
        for target in blocked_valves_ele:
            pressure = calc_pressure(0, 26, 'AA', target, tuple(blocked_valves_ele))
            max_pressure_ele = max(max_pressure_ele, pressure)
            print(f'E {blocked_valves_ele} -> {target}: {pressure}')

        max_pressure_total = max_pressure_you + max_pressure_ele
        max_pressure_part2 = max(max_pressure_part2, max_pressure_total)
        print (f'M {max_pressure_you} {max_pressure_ele} {max_pressure_total}')

print("Score part 2:", max_pressure_part2)

print("*** Scores ***")
print("Score part 1:", max_pressure_part1)
print("Score part 2:", max_pressure_part2)