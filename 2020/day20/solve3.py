import sys
import itertools
import math
import collections

groups = open(f"data{sys.argv[1]}.txt").read().split('\n\n')


def rotate(lines, rotations):
	new_lines = lines
	for r in range(rotations):
		new_lines = list(zip(*new_lines[::-1]))
	return new_lines

def flip(lines):
	return lines[::-1]

def binary_list_to_decimal(binary_list):
	string = ''.join(map(str, binary_list))
	decimal = int(string, 2)
	return decimal


# Parse the data
border_tiles = dict()
pixel_tiles = dict()
for group in groups:
	# Id
	id = int(group[5:9])
	print('id', id, '\n')

	# Lines
	lines = group.split('\n')[1:]
	lines = [line.replace('.', '0') for line in lines]
	lines = [line.replace('#', '1') for line in lines]
	lines = [[int(char) for char in line] for line in lines]
	for line in lines: print(line)
	print('\n')

	# Pixels: store the pixels for the 8 possible poses per tile
	pixels_per_pose = {
		'DEF': lines,
		'RO1': rotate(lines, 1),
		'RO2': rotate(lines, 2),
		'RO3': rotate(lines, 3),
		'FLI': flip(lines),
		'FR1': rotate(flip(lines), 1),
		'FR2': rotate(flip(lines), 2),
		'FR3': rotate(flip(lines), 3),
	}

	# Borders: calculate the unique value per border per pose
	for pose_id, lines in pixels_per_pose.items():
		AB = lines[0] # Top
		BC = [line[9] for line in lines] # Right
		DC = lines[9] # Bottom
		AD = [line[0] for line in lines] # Left
		borders = [binary_list_to_decimal(border) for border in [AB, BC, DC, AD]]

		# Store
		tile_id = str(id) + '-' + pose_id
		pixel_tiles[tile_id] = lines
		border_tiles[tile_id] = borders

	# for id, pixel_tile in pixel_tiles.items(): print(id, pixel_tile)
	# print('\n')
	for id, border_tile in border_tiles.items(): print(id, border_tile)
	print('\n')


# Part 1
all_borders = list(itertools.chain(*list(border_tiles.values())))

corner_ids = set()
for id, borders in border_tiles.items():
	count = sum([all_borders.count(border) for border in borders])
	if count == 24:
		corner_ids.add(int(id[0:4]))
print(corner_ids)
print('Answer 1:', math.prod(corner_ids), '\n')


# Part 2
# Get top left corner
for id, [top, right, bottom, left] in border_tiles.items():
	is_top_left_corner = True

	for search_id, [top2, right2, bottom2, left2] in border_tiles.items():
		if (top == bottom2 or left == right2) and not id[0:4] == search_id[0:4]:
			is_top_left_corner = False
	
	if is_top_left_corner:
		start_id = id		
		break
print("Top left corner:", start_id)

# Map tiles to image grid
def print_image_grid(image_grid):
	for y, row in enumerate(image_grid):
		for x, id in enumerate(row):
			if not id: id = '--------'
			print(id, end=' ')
		print('')
	print('')

grid_width = int(math.sqrt(len(border_tiles) // 8))
image_grid = [[None for x in range(grid_width)] for y in range(grid_width)]
image_grid[0][0] = start_id
print(f"Starting at tile {start_id}")
print_image_grid(image_grid)

# Set search_tiles
search_tiles = border_tiles
search_tiles = {id:search_tiles[id] for id in search_tiles if id[0:4] != start_id[0:4]}
side_names = {0: 'top', 1: 'right', 2: 'bottom', 3: 'left'}

def find_tile_id_by_border(search_tiles, border_id, border_position):
	side_name = side_names.get(border_position)
	for search_id, search_borders in search_tiles.items():
		search_border_id = search_borders[border_position] # border_position 0: top, 1: right, 2: bottom, 3: left
		if border_id == search_border_id:
			tile_id = search_id
			print(f"Found! Border {border_id} at tile {tile_id} on the {side_name}")
			return tile_id
	return None

def find_new_tile_and_pos(image_grid, search_tiles):
	for y, row in enumerate(image_grid):
		for x, id in enumerate(row):
			if not id:
				continue

			for border_position, border in enumerate(border_tiles[id]):
				new_y = y
				new_x = x
				new_tile_id = None

				if border_position == 1: # right
					lookup_position = 3 # left
					new_x += 1
					new_tile_id = find_tile_id_by_border(search_tiles, border, lookup_position)
				elif border_position == 2: # bottom
					lookup_position = 0 # top
					new_y += 1
					new_tile_id = find_tile_id_by_border(search_tiles, border, lookup_position)

				if new_tile_id:
					return new_tile_id, new_y, new_x
	return None, None, None

while True:
	print_image_grid(image_grid)
	new_tile_id, new_y, new_x = find_new_tile_and_pos(image_grid, search_tiles)

	if new_tile_id:
		image_grid[new_y][new_x] = new_tile_id
		search_tiles = {id:search_tiles[id] for id in search_tiles if id[0:4] != new_tile_id[0:4]}
	else:
		print('Image grid done!')
		print('')
		break

# Convert image grid to image pixels
def print_image(image):
	for y in image:
		for x in y:
			print(x, end='')
		print('')

image_width = len(image_grid) * 8
image = [[9 for x in range(image_width)] for y in range(image_width)]

for y, row in enumerate(image_grid):
	for x, id in enumerate(row):
		for y2, pixel_row in enumerate(pixel_tiles[id][1:9]):
			for x2, pixel in enumerate(pixel_row[1:9]):
				image[y*8 + y2][x*8 + x2] = pixel
print_image(image)
print('')
print('Image pixels done!')
print('')		

# Find seamonsters
print('Searching for this monster...')
print('')
print('                   1 ')
print(' 1    11    11    111')
print('  1  1  1  1  1  1   ')
print('')

monster = [
	[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9],
	[1, 9, 9, 9, 9, 1, 1, 9, 9, 9, 9, 1, 1, 9, 9, 9, 9, 1, 1, 1],
	[9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 1, 9, 9, 9],
]

def explore(image, monster, x, y):
    for delta_y, row in enumerate(monster):
        for delta_x, monster_char in enumerate(row):
            try:
                image_char = image[y + delta_y][x + delta_x]
                if monster_char == 1 and image_char != 1:
                    return False
            except:
                return False
    return True

def find_monster_in_image(image, monster):
	count_catch = 0
	for y, row in enumerate(image):
		for x, char in enumerate(row):
			# print(x, y, char)
			if explore(image, monster, x, y):
				print(f"Found monster at {x}, {y}")
				count_catch += 1
	return count_catch

while True:
	count_catch = find_monster_in_image(image, monster)
	monster_active_waters = 15 * count_catch

	if count_catch > 0:
		print(f"{count_catch} monsters found, making {monster_active_waters} waters active")
		print('')
		break

	image = rotate(image, 1)

active_waters = sum([sum(line) for line in image])
free_active_waters = active_waters - monster_active_waters
print(f"The sea has {active_waters} active waters, of which {free_active_waters} are not part of a sea monster")