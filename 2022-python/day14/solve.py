# Part 1
# Constants for the source of sand
source_x = 500
source_y = 0

# Function to parse rock paths and determine the cave's structure
def parse_rock_paths(rock_paths):
    max_x = 0
    max_y = 0
    for path in rock_paths:
        points = path.split(' -> ')
        for point in points:
            x, y = map(int, point.split(','))
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    cave = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for path in rock_paths:
        points = path.split(' -> ')
        x1, y1 = map(int, points[0].split(','))
        for i in range(1, len(points)):
            x2, y2 = map(int, points[i].split(','))
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    cave[y][x1] = '#'
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    cave[y1][x] = '#'
            x1, y1 = x2, y2
    return cave

def simulate_sand_falling(cave):
    units_of_sand = 0  # Counter to keep track of the units of sand that have come to rest
    x, y = source_x, source_y  # Starting position of the sand

    while True:
        # Check if the tile below is empty (air) and move down if possible
        if y + 1 < len(cave) and cave[y + 1][x] == '.':
            y += 1
            continue

        # Check if the tile diagonally down-left is empty and move down-left if possible
        # Note: The tile immediately to the left does not need to be empty
        if y + 1 < len(cave) and x - 1 >= 0 and cave[y + 1][x - 1] == '.':
            x -= 1
            y += 1
            continue

        # Check if the tile diagonally down-right is empty and move down-right if possible
        # Note: The tile immediately to the right does not need to be empty
        if y + 1 < len(cave) and x + 1 < len(cave[0]) and cave[y + 1][x + 1] == '.':
            x += 1
            y += 1
            continue

        # If all three possible destinations are blocked, the sand comes to rest
        cave[y][x] = 'o'
        units_of_sand += 1

        # If the sand has reached the bottom of the cave, break the loop
        if y + 1 == len(cave):
            break

        # Reset the position of the sand to the source for the next unit
        x, y = source_x, source_y

    return units_of_sand - 1  # Subtract 1 to account for the first sand hitting the abyss

# Read rock paths from file
rock_paths = []
with open('data2.txt', 'r') as file:
    for line in file:
        rock_paths.append(line.strip())

# Parse the rock paths to get the cave structure
cave = parse_rock_paths(rock_paths)

# Simulate the sand falling with the cave structure
units_of_sand_at_rest = simulate_sand_falling(cave)

# Function to draw the cave
def draw_cave(cave):
    start_col = int(len(cave[0]) * 0.4)  # Starting from the 40% mark to get the right 60%
    for row in cave:
        print(''.join(row[start_col:]))
draw_cave(cave)
print(units_of_sand_at_rest)