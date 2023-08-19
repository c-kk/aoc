import copy

SHAPES = [
    [(0,0), (0,1), (0,2), (0,3)], # plain
    [(0,1), (1,0), (1,1), (1,2), (2,1)], # cross
    [(0,2), (1,2), (2,0), (2,1), (2,2)], # wally
    [(0,0), (1,0), (2,0), (3,0)], # longo
    [(0,0), (0,1), (1,0), (1,1)] # block    
]

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
JET_DIRECTIONS = list(open(filename).read())
LEN_JET_DIRECTIONS = len(JET_DIRECTIONS)

def print_grid(grid, shape, shape_pos_y, shape_pos_x):
    draw_grid = copy.deepcopy(grid)
    if shape:
        for point_y, point_x in shape:
            draw_grid[shape_pos_y + point_y][shape_pos_x + point_x] = '@'
    for row in draw_grid:
        print(''.join(row))

def get_tower_height(grid):
    grid_height = len(grid) - 1
    available_height = next((i for i, row in enumerate(grid) if row != ['|', '.', '.', '.', '.', '.', '.', '.', '|']), len(grid))
    tower_height = grid_height - available_height
    return tower_height

def add_and_move_rock(_grid, _shape_index, _jet_index):
    # Add new shape to grid
    _shape_index += 1
    if _shape_index == 5:
        _shape_index = 0
    shape = SHAPES[_shape_index]

    # print(f'Rock {i} begins falling')
    shape_height = max([coord[0] for coord in shape]) + 1
    shape_pos_y = 0
    shape_pos_x = 3

    needed_height = shape_height + 3
    available_height = next((i for i, row in enumerate(_grid) if row != ['|', '.', '.', '.', '.', '.', '.', '.', '|']), len(_grid))
    
    if available_height < needed_height:
        height_to_add = needed_height - available_height
        for _ in range(0, height_to_add):
            _grid.insert(0, ['|', '.', '.', '.', '.', '.', '.', '.', '|'])
    elif available_height > needed_height:
        height_to_remove = available_height - needed_height
        for _ in range(0, height_to_remove):
            _grid.pop(0)
    
    while shape:
        # Blow the jet
        _jet_index += 1
        if _jet_index == LEN_JET_DIRECTIONS:
            _jet_index = 0
        jet_direction = JET_DIRECTIONS[_jet_index]

        if jet_direction == '>':
            can_move_right = all([_grid[shape_pos_y + point_y][shape_pos_x + point_x + 1] == '.' for point_y, point_x in shape])
            if can_move_right:
                # print('Jet pushes rock right')
                shape_pos_x += 1
            # else:
                # print('Jet pushes rock right, but nothing happens')
        elif jet_direction == '<':
            can_move_left = all([_grid[shape_pos_y + point_y][shape_pos_x + point_x - 1] == '.' for point_y, point_x in shape])
            if can_move_left:
                # print('Jet pushes rock left')
                shape_pos_x -= 1
            # else:
                # print('Jet pushes rock left, but nothing happens')

        # Move shape down or freeze it
        can_move_down = all([_grid[shape_pos_y + point_y + 1][shape_pos_x + point_x] == '.' for point_y, point_x in shape])
        if can_move_down:
            # print('Rock falls 1 unit')
            shape_pos_y += 1
        else:
            # print('Rock comes to rest')
            for point_y, point_x in shape:
                _grid[shape_pos_y + point_y][shape_pos_x + point_x] = '#'
            shape = None
    return _grid, _shape_index, _jet_index

grid = [['+', '-', '-', '-', '-', '-', '-', '-', '+']]
shape_index = -1
jet_index = -1

for rock_index in range (0, 2022):
    grid, shape_index, jet_index = add_and_move_rock(grid, shape_index, jet_index)

score_part1 = get_tower_height(grid)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

grid = [['+', '-', '-', '-', '-', '-', '-', '-', '+']]
rock_index = -1
shape_index = -1
jet_index = -1
found_jet_indexes = dict()

print('Find pattern')
while True:
    rock_index += 1
    grid, shape_index, jet_index = add_and_move_rock(grid, shape_index, jet_index)

    if shape_index == 0:
        if not jet_index in found_jet_indexes:
            found_jet_indexes[jet_index] = rock_index, get_tower_height(grid)
        else:
            pattern_starts_at_rock_index, height_when_pattern_starts = found_jet_indexes[jet_index]
            pattern_repeats_every = rock_index - pattern_starts_at_rock_index
            tower_height = get_tower_height(grid)
            height_per_repeat = tower_height - height_when_pattern_starts

            print('Rock', pattern_starts_at_rock_index, 'Shape', shape_index, 'Jet', jet_index, 'Height', height_when_pattern_starts)
            print('Rock', rock_index, 'Shape', shape_index, 'Jet', jet_index, 'Height', tower_height)
            print('Pattern repeats every', pattern_repeats_every, 'rocks')
            print('Height per repeat', height_per_repeat)
            break

print('Calculate total tower height')
total_tower_height = height_when_pattern_starts
print('1. Start with height when pattern starts => Total tower height', total_tower_height)

# 2. Add the repeats
repeats = (1000000000000 - pattern_starts_at_rock_index - 1) // pattern_repeats_every
height_of_repeats = repeats * height_per_repeat
total_tower_height += height_of_repeats
print('2. Add height', height_of_repeats, 'for', repeats, 'pattern repeats => Total tower height', total_tower_height)

# 3. Add the leftover
rocks_leftover = (1000000000000 - pattern_starts_at_rock_index - 1) % pattern_repeats_every
for _ in range(rocks_leftover):
    rock_index += 1
    grid, shape_index, jet_index = add_and_move_rock(grid, shape_index, jet_index)

height_of_leftover = get_tower_height(grid) - tower_height
total_tower_height += height_of_leftover
print('3. Add height', height_of_leftover, 'for', rocks_leftover, 'rocks leftover after the repeats => Total tower height', total_tower_height)

score_part2 = total_tower_height
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)