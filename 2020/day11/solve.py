lines = open("2020/day11/data.txt").read().split('\n')

seats = {}
for y, line in enumerate(lines):
    for x, character in enumerate(line):
        seats[(x, y)] = character

# Part 1
is_finished = False
new_seats = seats.copy()

while not is_finished:
    is_finished = True
    sts = new_seats.copy()
    new_seats = {}

    for (x, y), character in sts.items():
        adjacent_seats = [
            sts.get((x-1, y-1), '.'),
            sts.get((x, y-1), '.'),
            sts.get((x+1, y-1), '.'),
            sts.get((x-1, y), '.'),
            sts.get((x+1, y), '.'),
            sts.get((x-1, y+1), '.'),
            sts.get((x, y+1), '.'),
            sts.get((x+1, y+1), '.'),
        ]

        count_occupied_adjecent = adjacent_seats.count('#')

        if character == '.':
            new_seats[(x, y)] = '.'

        elif character == 'L' and count_occupied_adjecent == 0:
            new_seats[(x, y)] = '#'
            is_finished = False

        elif character == '#' and count_occupied_adjecent >= 4:
            new_seats[(x, y)] = 'L'
            is_finished = False

        else:
            new_seats[(x, y)] = character

answer1 = list(new_seats.values()).count('#')
print(answer1)

# Part 2
def seat_in_direction(start_x, start_y, dx, dy, _seats):
    seat_x = start_x
    seat_y = start_y

    while True:
        seat_x += dx
        seat_y += dy
        key = (seat_x, seat_y)
        if key not in _seats:
            return '.'

        char = _seats.get(key)
        if char == '.':
            continue
        if char == 'L':
            return 'L'
        if char == '#':
            return '#'

is_finished = False
new_seats = seats.copy()

while not is_finished:
    is_finished = True
    sts = new_seats.copy()
    new_seats = {}

    for (x, y), character in sts.items():
        adjacent_seats = [
            seat_in_direction(x, y, -1, -1, sts),
            seat_in_direction(x, y, 0, -1, sts),
            seat_in_direction(x, y, 1, -1, sts),
            seat_in_direction(x, y, -1, 0, sts),
            seat_in_direction(x, y, 1, 0, sts),
            seat_in_direction(x, y, -1, 1, sts),
            seat_in_direction(x, y, 0, 1, sts),
            seat_in_direction(x, y, 1, 1, sts),
        ]

        count_occupied_adjecent = adjacent_seats.count('#')

        if character == '.':
            new_seats[(x, y)] = '.'

        elif character == 'L' and count_occupied_adjecent == 0:
            new_seats[(x, y)] = '#'
            is_finished = False

        elif character == '#' and count_occupied_adjecent >= 5:
            new_seats[(x, y)] = 'L'
            is_finished = False

        else:
            new_seats[(x, y)] = character

answer2 = list(new_seats.values()).count('#')
print(answer2)