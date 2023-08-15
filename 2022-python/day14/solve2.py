# Part 2
# Constants for the source of sand
source_x = 500
source_y = 0

# Function to parse rock paths and determine the cave's structure
def parse_rock_paths(rock_paths):
    max_y = max(max(int(point.split(',')[1]) for point in path.split(' -> ')) for path in rock_paths)
    floor_y = max_y + 2
    cave = [['.' for _ in range(source_x + 500)] for _ in range(floor_y + 1)]
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
    cave[floor_y] = ['#' for _ in range(source_x + 500)]  # Add the floor
    return cave

def simulate_sand_falling(cave):
    units_of_sand = 0
    x, y = source_x, source_y
    while True:
        # Check if the source of the sand becomes blocked
        if y == source_y and cave[y][x] != '.':
            break

        # Check if the tile below is empty (air) and move down if possible
        if y + 1 < len(cave) and cave[y + 1][x] == '.':
            y += 1
            continue

        # Check if the tile diagonally down-left is empty and move down-left if possible
        if y + 1 < len(cave) and x - 1 >= 0 and cave[y + 1][x - 1] == '.':
            x -= 1
            y += 1
            continue

        # Check if the tile diagonally down-right is empty and move down-right if possible
        if y + 1 < len(cave) and x + 1 < len(cave[0]) and cave[y + 1][x + 1] == '.':
            x += 1
            y += 1
            continue

        # If all three possible destinations are blocked, the sand comes to rest
        cave[y][x] = 'o'
        units_of_sand += 1

        # Reset the position of the sand to the source for the next unit
        x, y = source_x, source_y

    return units_of_sand

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
    for row in cave:
        print(''.join(row))
draw_cave(cave)
print(units_of_sand_at_rest)
