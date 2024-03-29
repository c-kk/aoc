import re
from itertools import permutations

def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
CUBES = set([tuple(string_to_numbers(line)) for line in lines])
AXIS_MIN_MAX = [(min(cube[i] for cube in CUBES), max(cube[i] for cube in CUBES)) for i in range(3)]
DIRECTIONS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

# Part 1
print("*** Part 1 ***")
def count_visible_sides(cubes):
    visible_side_count = 0
    for x in range(AXIS_MIN_MAX[0][0], AXIS_MIN_MAX[0][1] + 1):
        for y in range(AXIS_MIN_MAX[1][0], AXIS_MIN_MAX[1][1] + 1):
            for z in range(AXIS_MIN_MAX[2][0], AXIS_MIN_MAX[2][1] + 1):
                for dx, dy, dz in DIRECTIONS:
                    cube = (x, y, z)
                    if cube in cubes and (x + dx, y + dy, z + dz) not in cubes:
                        visible_side_count += 1
    return visible_side_count

score_part1 = count_visible_sides(CUBES)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

# Add a layer of possible water cubes around the area with cubes
possible_water_cubes = set()
for x in range(AXIS_MIN_MAX[0][0] - 1, AXIS_MIN_MAX[0][1] + 2):
    for y in range(AXIS_MIN_MAX[1][0] - 1, AXIS_MIN_MAX[1][1] + 2):
        for z in range(AXIS_MIN_MAX[2][0] - 1, AXIS_MIN_MAX[2][1] + 2):
            possible_water_cube = (x, y, z)
            if possible_water_cube not in CUBES:
                possible_water_cubes.add(possible_water_cube)

# Start expanding water from the bottom corner
water_cubes_to_check = [(AXIS_MIN_MAX[0][0] - 1, AXIS_MIN_MAX[1][0] - 1, AXIS_MIN_MAX[2][0] - 1)]

# Expand water until there are no more possible water cubes
while water_cubes_to_check:
    water_cube_to_check = water_cubes_to_check.pop()
    x,y,z = water_cube_to_check
    for dx, dy, dz in DIRECTIONS:
        cube_adjacent = (x + dx, y + dy, z + dz)
        if cube_adjacent in possible_water_cubes:
            water_cubes_to_check.append(cube_adjacent)
            possible_water_cubes.remove(cube_adjacent)

# The possible water cubes left are the airgapped cubes
print(f"Airgapped cubes count: {len(possible_water_cubes)}")
print(f"Regular cubes count: {len(CUBES)}")

# Merge the cubes and airgapped cubes and count the visible sides
cubes_and_airgapped_cubes = CUBES.union(possible_water_cubes)
score_part2 = count_visible_sides(cubes_and_airgapped_cubes)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)