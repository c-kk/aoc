import re
import copy
from itertools import chain

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
            map_dict[(y, x)] = item

# Functions
def print_map(map_for_print):
    for y in range(max_col_length):
        for x in range(max_row_length):
            print(map_for_print[(y, x)] if (y, x) in map_for_print else ' ', end='')
        print()

def move_in_list(lst, item, steps): 
    return lst[(lst.index(item) + steps) % len(lst)]

def move_in_lists(lsts, item, steps):
    for lst in lsts:
        if item in lst: 
            return move_in_list(lst, item, steps)

def follow_the_path(path, xrows, ycols):
    # Make a copy of the map dictionary for printing 
    map_for_print = map_dict.copy()

    # Start at the top left non-space corner, facing right
    y_x = xrows[0][0]
    facing = '>'
    map_for_print[y_x] = facing

    # Follow the path
    for action in path:
        if action == 'R' or action == 'L': 
            facing = move_in_list(facings, facing, 1 if action == 'R' else -1)
            map_for_print[y_x] = facing
        else:
            for _ in range(action):
                if   facing == '>': next_y_x = move_in_lists(xrows, y_x, 1)
                elif facing == '<': next_y_x = move_in_lists(xrows, y_x, -1)
                elif facing == 'v': next_y_x = move_in_lists(ycols, y_x, 1)
                elif facing == '^': next_y_x = move_in_lists(ycols, y_x, -1)
                if map_dict[next_y_x] != '#': y_x = next_y_x
                map_for_print[y_x] = facing

    print_map(map_for_print)

    # Return score
    return 1000 * (y_x[0] + 1) + 4 * (y_x[1] + 1) + {'>': 0, 'v': 1, '<': 2, '^': 3}[facing]

print("*** Part 1 ***")
# Precompute lists of non-space elements in each row and column
xrows_part1 = [[(y, x) for x in range(max_row_length) if (y, x) in map_dict] for y in range(max_col_length)]
ycols_part1 = [[(y, x) for y in range(max_col_length) if (y, x) in map_dict] for x in range(max_row_length)]
score_part1 = follow_the_path(path, xrows_part1, ycols_part1)
print("Score part 1:", score_part1)

print("*** Part 2 ***")
map_for_print = map_dict.copy()
print_map(map_for_print)
print()

# Precompute lists of non-space elements in each row and column
xrows_part2 = [[(y, x) for x in range(max_row_length) if (y, x) in map_dict] for y in range(max_col_length)]
ycols_part2 = [[(y, x) for y in range(max_col_length) if (y, x) in map_dict] for x in range(max_row_length)]

def rotate_face_clockwise(face, times):
    def rotate_90_clockwise(mat):
        return [list(row) for row in zip(*mat[::-1])]
    
    # def rotate_90_counter_clockwise(mat):
    #     return [list(row[::-1]) for row in zip(*mat)]
    
    for _ in range(times):
        # if direction == "clockwise":
        face = rotate_90_clockwise(face)
        # elif direction == "counter-clockwise":
        #     face = rotate_90_counter_clockwise(face)
    return face

def add_faces(*args):
    return [list(chain(*rows)) for rows in zip(*args)]

def print_face(face):
    for row in face:
        for element in row:
            character = map_dict[element]
            print(element, end='')
        print()

def print_faces(faces):
    for face_pos, face in faces:
        print("fase_pos", face_pos)
        print_face(face)
        print()

def select_face(start_y, start_x, face_size):
    return [[(y, x) for x in range(start_x, start_x + face_size)] for y in range(start_y, start_y + face_size)]

face_size = 4
faces = []
faces.append([(0,2), select_face(0, 8, face_size)])
faces.append([(1,0), select_face(4, 0, face_size)])
faces.append([(1,1), select_face(4, 4, face_size)])
faces.append([(1,2), select_face(4, 8, face_size)])
faces.append([(2,2), select_face(8, 8, face_size)])
faces.append([(2,3), select_face(8, 12, face_size)])
print_faces(faces)
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