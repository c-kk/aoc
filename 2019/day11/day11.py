import numpy as np
import luca
import time

def print_tiles(tiles, robot_pos, fac, lines_printed):
	for line in range(lines_printed):
		print("\033[F", end='')

	keys = np.array(list(tiles.keys()))
	xs = keys[:,0]
	ys = keys[:,1]
	xmin, xmax = min(xs), max(xs)
	ymin, ymax = min(ys), max(ys)

	ymin = max(robot_pos[1] - 25, ymin)
	ymax = min(robot_pos[1] + 25, ymax)

	lines_printed = 0
	for y in range(ymax, ymin-1, -1):
		for x in range(xmin, xmax+1):
			tile_pos = (x,y)
			color = tiles.get(tile_pos, 0)
			if color == 0:
				paint = ' '
			elif color == 1:
				paint = '█'

			if robot_pos == tile_pos:
				paint = "^>v<"[fac]

			print(paint, end='')
		print()
		lines_printed += 1

	return lines_printed

def paint(start_color, sleep_time):
	paint_ai = luca.Program(
		des='Day 11 part 1 - Paint AI',
		mem=[3,8,1005,8,320,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,29,2,1005,1,10,1006,0,11,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,57,1,8,15,10,1006,0,79,1,6,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,90,2,103,18,10,1006,0,3,2,105,14,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,123,2,9,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,150,1,2,2,10,2,1009,6,10,1,1006,12,10,1006,0,81,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,187,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,209,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,231,1,1008,11,10,1,1001,4,10,2,1104,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,264,1,8,14,10,1006,0,36,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,293,1006,0,80,1006,0,68,101,1,9,9,1007,9,960,10,1005,10,15,99,109,642,104,0,104,1,21102,1,846914232732,1,21102,1,337,0,1105,1,441,21102,1,387512115980,1,21101,348,0,0,1106,0,441,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,209533824219,1,1,21102,1,395,0,1106,0,441,21101,0,21477985303,1,21102,406,1,0,1106,0,441,3,10,104,0,104,0,3,10,104,0,104,0,21101,868494234468,0,1,21101,429,0,0,1106,0,441,21102,838429471080,1,1,21102,1,440,0,1106,0,441,99,109,2,21201,-1,0,1,21101,0,40,2,21102,472,1,3,21101,0,462,0,1106,0,505,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,467,468,483,4,0,1001,467,1,467,108,4,467,10,1006,10,499,1102,1,0,467,109,-2,2106,0,0,0,109,4,2101,0,-1,504,1207,-3,0,10,1006,10,522,21101,0,0,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21102,541,1,0,1106,0,546,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,569,2207,-4,-2,10,1006,10,569,22102,1,-4,-4,1105,1,637,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,588,1,0,1105,1,546,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,607,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,629,21201,-1,0,1,21102,629,1,0,105,1,504,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0],
		)

	moves = {
		0: (0, 1),  # Up
		1: (1, 0),  # Right
		2: (0, -1), # Down
		3: (-1, 0)  # Left
	}

	pos = (0, 0)
	fac = 0
	tiles = {}
	tiles[pos] = start_color
	lines_printed = 0

	while True:
		current_color = tiles.get(pos, 0)
		paint_ai.inp = [current_color]

		paint_ai = luca.run(paint_ai, debug=False)

		[nw_color, rotate] = paint_ai.out
		paint_ai.out = []

		tiles[pos] = nw_color
		
		if rotate == 0:
			fac = (fac - 1) % 4
		elif rotate == 1:
			fac = (fac + 1) % 4

		move = moves[fac]
		pos = tuple(np.add(pos, move))

		lines_printed = print_tiles(tiles, pos, fac, lines_printed)
		time.sleep(sleep_time)

		if paint_ai.opc == 99:
			break

	return tiles

# Part 1
print(f'Part 1. Let\'s paint our spaceship using Elves AI!')
print(f'Starting on a black tile...')
tiles = paint(start_color=0, sleep_time=0)
count_painted = len(tiles)
print(f'Oh nootjes, the Elves AI went CRAZY')
print(f'Answer part 1: {count_painted}')
print('')
time.sleep(2)

# Part 2
print(f'Part 2. Let\'s try again!')
print(f'Now starting on a white tile...')
tiles = paint(start_color=1, sleep_time=0.02)
count_painted = len(tiles)