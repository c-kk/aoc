import collections
import math
import sys
import re
import copy
import time
import numpy as np

mdict = {
    'e':   (2, 0),
    'w':  (-2, 0),
    'ne':  (1, 2),
    'se':  (1,-2),
    'nw': (-1, 2),
    'sw': (-1,-2),
}

def import_data():
    ls = open(f"data{sys.argv[1]}.txt").read().split('\n')
    lines = []
    for l in ls:
        ms = []
        m = ""
        for c in l:
            m += c
            if m in ['e', 'se', 'sw', 'w', 'nw', 'ne']:
                move = mdict.get(m)
                ms.append(move)
                m = ""
        lines.append(ms)
    return lines

# Part 1
lines = import_data()
for line in lines: print(line)

tiles = dict()
for line in lines:
    curr = (0, 0)
    print(curr)
    for move in line:
        curr = tuple(np.add(curr, move))
        print(curr)

    if curr in tiles:
        del tiles[curr]
    else:
        tiles[curr] = 'b'
    print(f'tiles: {tiles} \n')

count = len(tiles)
print('Answer 1:', count)

# Part 2

# Loop through the days
for day in range(1, 101):
    # print(f'Day {day}')

    # Make tiles and add extra white border 
    ntiles = np.array(list(tiles.keys()))
    xs = ntiles[:,0]
    ys = ntiles[:,1]
    min_x, max_x = min(xs) - 1, max(xs) + 1
    min_y, max_y = min(ys) - 2, max(ys) + 2
    new_tiles = dict()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1, 2):
            curr = (x,y)
            count = 0
            for move in mdict.values():
                side = tuple(np.add(curr, move))
                if side in tiles:
                    if tiles[side] == 'b':
                        count += 1

            if curr in tiles:
                if tiles[curr] == 'b':
                    if count == 0 or count > 2:
                        new_tiles[curr] = 'w'
                    else:
                        new_tiles[curr] = 'b'

                elif tiles[curr] == 'w':
                    if count == 2:
                        new_tiles[curr] = 'b'
                    else:
                        new_tiles[curr] = 'w'

            elif curr not in tiles:
                if count == 2:
                    new_tiles[curr] = 'b'

            # print(curr, new_tiles.get(curr, None), count)

    count_b = list(tiles.values()).count('b')
    print('Day', day, min_x, max_x, min_y, max_y, count_b)
    tiles = new_tiles
    # time.sleep(3)

print(list(tiles.values()).count('b'))



