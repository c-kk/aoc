import re
import copy
from itertools import chain

# Helper functions
def tile_id(y, x):
    return 1000 * (y + 1) + 4 * (x + 1)

def print_map(map_for_print):
    for y in range(max_col_length):
        for x in range(max_row_length):
            print(map_for_print[tile_id(y,x)] if tile_id(y,x) in map_for_print else ' ', end='')
        print()

def move_in_list(lst, item, steps): 
    return lst[(lst.index(item) + steps) % len(lst)]

def move_in_lists(lsts, item, steps):
    for lst in lsts:
        if item in lst: 
            return move_in_list(lst, item, steps)

# Import data
data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
rows = [list(line) for line in lines[0:-2]]
path = [int(item) if item.isdigit() else item for item in re.findall(r'(\d+|[RL])', lines[-1])]
facings = ['>', 'v', '<', '^']

# Make all rows equal length
max_row_length = max(len(row) for row in rows)
max_col_length = len(rows)
rows = [row + [' '] * (max_row_length - len(row)) for row in rows]

# Precompute map dictionary of non-space elements
map_dict = {}
for y, row in enumerate(rows):
    for x, item in enumerate(row):
        if item != ' ':
            map_dict[tile_id(y,x)] = item

def follow_the_path(path, xrows, ycols):
    # Make a copy of the map dictionary for printing 
    map_for_print = map_dict.copy()

    # Start at the top left non-space corner, facing right
    tile_id = xrows[0][0]
    facing = '>'
    map_for_print[tile_id] = facing

    # Follow the path
    for action in path:
        if action == 'R' or action == 'L': 
            facing = move_in_list(facings, facing, 1 if action == 'R' else -1)
            map_for_print[tile_id] = facing
        else:
            for _ in range(action):
                if   facing == '>': next_tile_id = move_in_lists(xrows, tile_id, 1)
                elif facing == '<': next_tile_id = move_in_lists(xrows, tile_id, -1)
                elif facing == 'v': next_tile_id = move_in_lists(ycols, tile_id, 1)
                elif facing == '^': next_tile_id = move_in_lists(ycols, tile_id, -1)
                if map_dict[next_tile_id] != '#': tile_id = next_tile_id
                map_for_print[tile_id] = facing

    print_map(map_for_print)

    # Return score
    return tile_id + {'>': 0, 'v': 1, '<': 2, '^': 3}[facing]

print("*** Part 1 ***")
# Precompute lists of non-space elements in each row and column
xrows_part1 = [[tile_id(y,x) for x in range(max_row_length) if tile_id(y,x) in map_dict] for y in range(max_col_length)]
ycols_part1 = [[tile_id(y,x) for y in range(max_col_length) if tile_id(y,x) in map_dict] for x in range(max_row_length)]
score_part1 = follow_the_path(path, xrows_part1, ycols_part1)
print("Score part 1:", score_part1)

print("*** Part 2 ***")
map_for_print = map_dict.copy()
print_map(map_for_print)
print()

# Precompute lists of non-space elements in each row and column
# xrows_part2 = [[(y, x) for x in range(max_row_length) if (y, x) in map_dict] for y in range(max_col_length)]
# ycols_part2 = [[(y, x) for y in range(max_col_length) if (y, x) in map_dict] for x in range(max_row_length)]

def rotate_face_clockwise(face, times):    
    for _ in range(times):
        face = [list(row) for row in zip(*face[::-1])]
    return face

# def add_faces(*args):
#     return [list(chain(*rows)) for rows in zip(*args)]

def select_face(start_y, start_x, face_size):
    return [[tile_id(y,x) for x in range(start_x, start_x + face_size)] for y in range(start_y, start_y + face_size)]

def print_face_tile_ids(face):
    for row in face:
        for tile_id in row:
            print(tile_id, end=' ')
        print()

def print_faces_tile_ids(faces):
    for face_pos, face in faces.items():
        print("fase_pos", face_pos)
        print_face_tile_ids(face)
        print()

def print_face_tile_value(face):
    for row in face:
        for tile_id in row:
            print(map_dict[tile_id], end='')
        print()

def print_faces_tile_values(faces):
    face_id_ys = [face_id[0] for face_id in faces.keys()]
    face_id_xs = [face_id[1] for face_id in faces.keys()]
    face_id_y_min = min(face_id_ys)
    face_id_y_max = max(face_id_ys)
    face_id_x_min = min(face_id_xs)
    face_id_x_max = max(face_id_xs)
    grid = [[' ' for x in range(face_id_x_min * 4, (face_id_x_max + 1) * 4)] for y in range(face_id_y_min * 4, (face_id_y_max + 1) * 4)]
     
    for (face_id_y, face_id_x), face in faces.items():
        for tile_y, row in enumerate(face):
            for tile_x, tile_id in enumerate(row):
                grid[face_id_y * 4 + tile_y][face_id_x * 4 + tile_x] = map_dict[tile_id]

    for row in grid:
        for element in row:
            print(element, end='')
        print()
    print()

face_size = 4
faces = {}
faces[(0,2)] = select_face(0, 8, face_size)
faces[(1,0)] = select_face(4, 0, face_size)
faces[(1,1)] = select_face(4, 4, face_size)
faces[(1,2)] = select_face(4, 8, face_size)
faces[(2,3)] = select_face(8, 12, face_size)
faces[(2,2)] = select_face(8, 8, face_size)
# print_faces_tile_ids(faces)
print_faces_tile_values(faces)

faces[(0,0)] = rotate_face_clockwise(faces[(0,2)], 2)
del faces[(0,2)]
print_faces_tile_values(faces)

faces[(1,3)] = rotate_face_clockwise(faces[(2,3)], 3)
del faces[(2,3)]
print_faces_tile_values(faces)

faces[(2,0)] = rotate_face_clockwise(faces[(2,2)], 2)
del faces[(2,2)]
print_faces_tile_values(faces)

exit()
# print(faces[0])
# print(faces[1])
# print(faces[2])
# exit()
# print_face(faces[2])
# print()
# print_face(rotate_face(faces[2], 1, 'clockwise'))
# print_face(rotate_face_clockwise(faces[2], 1))
# exit()

xrows_part2 = add_faces(
    faces[0],
    rotate_face_clockwise(faces[5], 2),
    rotate_face_clockwise(faces[4], 2),
    rotate_face_clockwise(faces[2], 1),
)

print_face(xrows_part2)

exit()

face1 = [['.', '.', '.', '.'],
         ['.', '#', '.', '.'],
         ['.', '.', '.', '.'],
         ['.', '.', '.', '#']]
print_face(face1)
print()

face1_rotated = rotate_face_clockwise(face1, 1, 'clockwise')
print_face(face1_rotated)

# score_part2 = follow_the_path(path, xrows_part2, ycols_part2)
score_part2 = 0
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
# https://www.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/
# https://github.com/DarthGandalf/advent-of-code/blob/master/2022/day22.jl