import re
import sys
import copy
import itertools
import math

groups = open(f"data{sys.argv[1]}.txt").read().split('\n\n')
# print("\n".join(groups))

tiles = dict()
for group in groups:
	print(group)
	print('\n')

	id = int(group[5:9])

	lines = group.split('\n')[1:]
	lines = [line.replace('.', '0') for line in lines]
	lines = [line.replace('#', '1') for line in lines]
	# print(lines)

	AB = lines[0]
	BA = AB[::-1]
	DC = lines[9]
	CD = DC[::-1]
	AD = ''.join([line[0] for line in lines])
	DA = AD[::-1]
	BC = ''.join([line[9] for line in lines])
	CB = BC[::-1]
	# print(f"{AB=}\n{BA=}\n{DC=}\n{CD=}\n{AD=}\n{DA=}\n{BC=}\n{CB=}")

	AB = int(AB, base=2)
	BA = int(BA, base=2)
	DC = int(DC, base=2)
	CD = int(CD, base=2)
	AD = int(AD, base=2)
	DA = int(DA, base=2)
	BC = int(BC, base=2)
	CB = int(CB, base=2)
	print(f"{AB=}\n{BA=}\n{DC=}\n{CD=}\n{AD=}\n{DA=}\n{BC=}\n{CB=}")

	tiles[id] = [
		[AB, DC, AD, BC],
		[DA, CB, DC, AB],
		[CD, BA, CB, DA],
		[BC, AD, BA, CD],
		[DC, AB, DA, CB],
		[CB, DA, CD, BA],
		[BA, CD, BC, AD],
		[AD, BC, AB, DC],
	]
	print(tiles[id])
	print('\n')

def border_exists(search_tiles, border):
	for search_tile_index, search_tile in search_tiles.items():
		for search_orientation in search_tile:
			if border in search_orientation:
				return True
	return False

bordercount = {2: [], 3: [], 4: []}
for tile_index, tile in tiles.items():
	max_borders = 0
	search_tiles = copy.deepcopy(tiles)
	search_tiles.pop(tile_index)

	for orientation in tile:
		found_borders = 0
		for border_index, border in enumerate(orientation):
			if border_exists(search_tiles, border):
				found_borders += 1
		max_borders = max(found_borders, max_borders)
	bordercount[max_borders].append(tile_index)
print(bordercount)

print(math.prod(bordercount[2]))


