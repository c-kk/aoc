data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
rows = [[char for char in line] for line in lines]

# Print map
def print_map(rows):
    for row in rows:
        for char in row:
            print(char, end='')
        print()

# Replace characters in rows
replacement_dict = {'|': '│', '-': '─', 'L': '└', 'J': '┘', '7': '┐', 'F': '┌'}
for row in rows:
    row[:] = [replacement_dict.get(char, char) for char in row]

# Add padding
rows = [[' '] + row + [' '] for row in rows]
rows = [[' '] * len(rows[0])] + rows + [[' '] * len(rows[0])]

# Map dicts
directions = {
    'north': (-1, 0),
    'east': (0, 1),
    'south': (1, 0),
    'west': (0, -1)
}

directions_opposites = {'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east'}

next_char_connects_dict = {
    '└': ['south', 'west'],
    '┘': ['south', 'east'],
    '┐': ['north', 'east'],
    '┌': ['north', 'west'],
    '│': ['south', 'north'],
    '─': ['east', 'west'],
    '.': [],
    ' ': []
}

char_exits_dict = {
    '└': ['north', 'east'],
    '┘': ['north', 'west'],
    '┐': ['south', 'west'],
    '┌': ['south', 'east'],
    '│': ['north', 'south'],
    '─': ['west', 'east']
}

# Part 1
print("*** Part 1 ***")

# Find start position and start char
for y, row in enumerate(rows):
    for x, char in enumerate(row):
        if char == 'S': 
            start_position = (y, x)

            exits_found = [direction for direction, (dy, dx) in directions.items() 
               if direction in next_char_connects_dict[rows[y + dy][x + dx]]]
                        
            for char, exits in char_exits_dict.items():
                if set(exits) == set(exits_found):
                    start_char = char
            
            print('Start position:', start_position, 'Start char:', start_char)        
                
# Replace S with start char
rows[start_position[0]][start_position[1]] = start_char
print_map(rows)

# Build loop
loop_positions = [start_position]
current_position = start_position
current_direction = char_exits_dict[start_char][0]

while True:
    dy, dx = directions[current_direction]
    next_position = (current_position[0] + dy, current_position[1] + dx)

    if next_position == start_position: break

    loop_positions.append(next_position)
    next_char = rows[next_position[0]][next_position[1]]
    next_char_connects = next_char_connects_dict[next_char]
    current_direction = directions_opposites[next_char_connects[0] if next_char_connects[0] != current_direction else next_char_connects[1]]
    current_position = next_position

score_part1 = int(len(loop_positions) / 2)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

# Remove pipes not in loop from rows
for row_index, row in enumerate(rows):
    for char_index, char in enumerate(row):
        if (row_index, char_index) not in loop_positions and char != ' ':
            rows[row_index][char_index] = '.'

# Add two extra rows after each row            
for row_index, row in enumerate(rows):
    if row_index % 3 == 0:
        rows.insert(row_index + 1, [' '] * len(row))
        rows.insert(row_index + 1, [' '] * len(row))

# Add two extra columns after each column
for row_index, row in enumerate(rows):
    for char_index, char in enumerate(row):
        if char_index % 3 == 0:
            rows[row_index].insert(char_index + 1, ' ')
            rows[row_index].insert(char_index + 1, ' ')

# Loop through rows and columns and extend the chars
extended_chars_dict = {
    '┌': [(1, 1), (1, 2), (2, 1)],
    '┐': [(1, 0), (1, 1), (2, 1)],
    '└': [(0, 1), (1, 1), (1, 2)],
    '┘': [(1, 0), (1, 1), (0, 1)],
    '│': [(0, 1), (1, 1), (2, 1)],
    '─': [(1, 0), (1, 1), (1, 2)],
}

for row_index, row in enumerate(rows):
    if row_index % 3 != 0: continue
    for char_index, char in enumerate(row):
        if char_index % 3 != 0: continue
        if char not in extended_chars_dict: continue
        rows[row_index][char_index] = ' '
        for delta in extended_chars_dict[char]:
            rows[row_index + delta[0]][char_index + delta[1]] = '#'

# Add all cells from the first and last row and column to cells to check for flooding
cells_to_check = set()
for column_index in range(len(rows[0])):
    cells_to_check.add((0, column_index))
    cells_to_check.add((len(rows) - 1, column_index))
for row_index in range(len(rows)):
    cells_to_check.add((row_index, 0))
    cells_to_check.add((row_index, len(rows[0]) - 1))

# Flood cells
width = len(rows[0])
height = len(rows)
to_check_count = len(cells_to_check)
while to_check_count > 0:
    cell_to_check = cells_to_check.pop()
    y, x = cell_to_check
    for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_y = y + delta[0]
        if new_y < 0 or new_y >= height: continue

        new_x = x + delta[1]
        if new_x < 0 or new_x >= width: continue

        current_char_in_new_cell = rows[new_y][new_x]
        if current_char_in_new_cell in ['#', '~']: continue

        # Flood cell
        rows[new_y][new_x] = '~'
        new_cell_to_check = (new_y, new_x)
        cells_to_check.add(new_cell_to_check)

    to_check_count = len(cells_to_check)

print_map(rows)

score_part2 = sum(char == '.' for row in rows for char in row)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)