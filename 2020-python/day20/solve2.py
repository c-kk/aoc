import re
import sys
import copy
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

	for id, pixel_tile in pixel_tiles.items(): print(id, pixel_tile)
	print('\n')
	for id, border_tile in border_tiles.items(): print(id, border_tile)
	print('\n')

	# print(border_tiles)

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
start_id = str(corner_ids.pop()) + '-DEF'
print(f"Starting at tile {start_id}")

# Map tiles to image grid
search_tiles = border_tiles
search_tiles = {id:search_tiles[id] for id in search_tiles if id[0:4] != start_id[0:4]}
image_grid = {(0,0): start_id}
side_names = {0: 'top', 1: 'right', 2: 'bottom', 3: 'left'}

def find_tile_id_by_border(search_tiles, border_id, border_position):
	side_name = side_names.get(border_position)
	for search_id, search_borders in search_tiles.items():
		search_border_id = search_borders[border_position] # border_position 0: top, 1: right, 2: bottom, 3: left
		if border_id == search_border_id:
			tile_id = search_id
			print(f"Found! Border {border_id} at tile {tile_id} on the {side_name}")
			return tile_id
	# print(f"Not found! Border {border_id} on the {side_name}")
	return None

def find_new_tile_and_pos(image_grid, search_tiles):
	for pos, id in image_grid.items():
		for border_position, border in enumerate(border_tiles[id]):
			# print(f"{pos} {id} has border {border} on the {side_names.get(border_position)}") 
			x, y = pos

			if border_position == 0: # top
				lookup_position = 2 # bottom
				y -= 1
			elif border_position == 1: # right
				lookup_position = 3 # left
				x += 1
			elif border_position == 2: # bottom
				lookup_position = 0 # top
				y += 1
			elif border_position == 3: # left
				lookup_position = 1 # right
				x -= 1

			new_tile_id = find_tile_id_by_border(search_tiles, border, lookup_position)
			if new_tile_id:
				new_pos = (x, y)
				# print(new_pos, new_tile_id)
				return new_tile_id, new_pos	
	return None, None

def print_image_grid(image_grid):
	xs = [key[0] for key in list(image_grid.keys())]
	ys = [key[1] for key in list(image_grid.keys())]

	for y in range(min(ys), max(ys)+1):
		for x in range(min(xs), max(xs)+1):
			value = image_grid.get((x,y), '--------')
			print(f"{value}", end=' ')
		print('')
	print('\n')

while True:
	print_image_grid(image_grid)
	new_tile_id, new_pos = find_new_tile_and_pos(image_grid, search_tiles)

	if new_tile_id:
		image_grid[new_pos] = new_tile_id
		search_tiles = {id:search_tiles[id] for id in search_tiles if id[0:4] != new_tile_id[0:4]}
	else:
		print('Image grid done!')
		print('\n')
		break

# Convert image grid to image pixels
def print_image(image):
	for y in image:
		for x in y:
			print(x, end='')
		print('')

grid_size = int(math.sqrt(len(image_grid)))
image_width = grid_size * 10
image = [[9 for x in range(image_width)] for y in range(image_width)]
# print_image(image)

# xs = [key[0] for key in list(image_grid.keys())]
# ys = [key[1] for key in list(image_grid.keys())]

# print(min(ys), max(ys), min(xs), max(xs))

# for y in range(min(ys), max(ys)+1):
# 	for x in range(min(xs), max(xs)+1):
# 		id = image_grid.get((x,y))
# 		print(id)





















