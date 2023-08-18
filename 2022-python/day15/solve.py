import re
def string_to_numbers(string): return [int(d) for d in re.findall("(-?\d+)", string)]
def manhattan_distance(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().strip().split('\n')

# Part 1
print("*** Part 1 ***")
sensors_beacons = []
beacons = set()
min_x = min_y = max_x = max_y = 0
for line in lines:
    (sensor_x, sensor_y, beacon_x, beacon_y) = string_to_numbers(line)
    sensors_beacons.append({"sensor": (sensor_x, sensor_y), "beacon": (beacon_x, beacon_y)})
    beacons.add((beacon_x, beacon_y))
    min_x = min(min_x, sensor_x, beacon_x)
    max_x = max(max_x, sensor_x, beacon_x)
    min_y = min(min_y, sensor_y, beacon_y)
    max_y = max(max_y, sensor_y, beacon_y)

# Calculate the no-beacon positions
no_beacons = set()
row = 10 if data_version != "2" else 2000000
print('Row', row)

for sensors_beacon in sensors_beacons:
    sensor_x = sensors_beacon["sensor"][0]
    sensor_y = sensors_beacon["sensor"][1]
    beacon_x = sensors_beacon["beacon"][0]
    beacon_y = sensors_beacon["beacon"][1]

    md = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
    
    y_distance_to_row = abs(sensor_y - row)
    x_distance_available = md - y_distance_to_row

    if x_distance_available >= 0:
        start_x = sensor_x - x_distance_available
        end_x = sensor_x + x_distance_available

        for no_beacon_x in range(start_x, end_x + 1):
            no_beacon = (no_beacon_x, row)
            if no_beacon not in beacons:
                no_beacons.add(no_beacon)
                    
def print_grid(sensors_beacons, no_beacons):
    grid = [['.' for _ in range(0, 1 + max_x - min_x)] for _ in range(0, 1 + max_y - min_y)]

    for sensors_beacon in sensors_beacons:
        sensor = sensors_beacon["sensor"]
        beacon = sensors_beacon["beacon"]
        print(sensor[1] - min_y, sensor[0] - min_x, beacon[1] - min_y, beacon[0] - min_x)
        
        grid[sensor[1] - min_y][sensor[0] - min_x] = 'S'
        grid[beacon[1] - min_y][beacon[0] - min_x] = 'B'

    for no_beacon in no_beacons:
        grid[no_beacon[1] - min_y][no_beacon[0] - min_x] = '#'

    for row in grid:
        print(''.join(row))
    
if data_version != "2":
    print_grid(sensors_beacons, no_beacons)

score_part1 = len(no_beacons)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

# Calculate the Manhattan distances for all sensors
mds = {(s_x, s_y): manhattan_distance((s_x, s_y), (b_x, b_y)) 
          for (s_x, s_y, b_x, b_y) in [string_to_numbers(line) for line in lines]}

# Calculate coefficients for all sensors by using the Manhattan distance as radius
a_coefficients, b_coefficients = set(), set()
for ((s_x, s_y), md) in mds.items():
    # Two lines with gradient 1
    a_coefficients.add(s_y - s_x + md + 1)
    a_coefficients.add(s_y - s_x - md - 1)

    # Two lines with gradient -1
    b_coefficients.add(s_x + s_y + md + 1)
    b_coefficients.add(s_x + s_y - md - 1)

# Find the intersection point
for a_coefficient in a_coefficients:
    for b_coefficient in b_coefficients:
        point_x = (b_coefficient - a_coefficient) // 2
        point_y = (a_coefficient + b_coefficient) // 2
        point = (point_x, point_y)

        if not(0 < point_x < 4000000 and 0 < point_y < 4000000):
            continue

        found = True
        for (sensor, md) in mds.items():
            if not(manhattan_distance(point, sensor) > md):
                found = False

        if found:
            score_part2 = 4000000 * point_x + point_y

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)