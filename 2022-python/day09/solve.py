lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0
tail_positions = {'0:0'}

for move in lines:
    direction,steps = move.split(' ')
    steps = int(steps)

    for i in range(steps):
        if direction == "R":
            head_x += 1
        elif direction == "L":
            head_x -= 1
        elif direction == "U":
            head_y += 1
        elif direction == "D":
            head_y -= 1

        # Move tail
        dif_x = head_x - tail_x
        dif_y = head_y - tail_y

        if dif_x > 1:
            tail_x += 1
            tail_y = head_y
        elif dif_x < -1:
            tail_x -= 1
            tail_y = head_y

        if dif_y > 1:
            tail_y += 1
            tail_x = head_x
        elif dif_y < -1:
            tail_y -= 1
            tail_x = head_x

        # Save tail position
        tail_positions.add(str(tail_x) + ':' + str(tail_y))
        score_part1 = len(tail_positions)

print("Score part 1:", score_part1)   

# Part 2
print("*** Part 2 ***")
score_part2 = 0

knots = []
for i in range(10):
    knots.append([0, 0])

min_head_x = 0
min_head_y = 0
max_head_x = 0
max_head_y = 0
tail_positions = {'0:0'}

for move in lines:
    direction,steps = move.split(' ')
    steps = int(steps)

    for i in range(steps):
        # Move head
        if direction == "R":
            knots[0][0] += 1
        elif direction == "L":
            knots[0][0] -= 1
        elif direction == "U":
            knots[0][1] += 1
        elif direction == "D":
            knots[0][1] -= 1

        # Move tail
        for knot_index in range(1, 10):
            dif_x = knots[knot_index - 1][0] - knots[knot_index][0]
            dif_y = knots[knot_index - 1][1] - knots[knot_index][1]

            if dif_x == 2:
                knots[knot_index][0] += 1
                if dif_y == 2:
                    knots[knot_index][1] += 1
                elif dif_y == -2:
                    knots[knot_index][1] -= 1
                else:
                    knots[knot_index][1] = knots[knot_index - 1][1]

            elif dif_x == -2:
                knots[knot_index][0] -= 1
                if dif_y == 2:
                    knots[knot_index][1] += 1
                elif dif_y == -2:
                    knots[knot_index][1] -= 1
                else:
                    knots[knot_index][1] = knots[knot_index - 1][1]

            elif dif_y == 2:
                knots[knot_index][1] += 1
                if dif_x == 2:
                    knots[knot_index][0] += 1
                elif dif_x == -2:
                    knots[knot_index][0] -= 1
                else:
                    knots[knot_index][0] = knots[knot_index - 1][0]

            elif dif_y == -2:
                knots[knot_index][1] -= 1
                if dif_x == 2:
                    knots[knot_index][0] += 1
                elif dif_x == -2:
                    knots[knot_index][0] -= 1
                else:
                    knots[knot_index][0] = knots[knot_index - 1][0]

        # Save tail position
        tail_positions.add(str(knots[9][0]) + ':' + str(knots[9][1]))
        score_part2 = len(tail_positions)

        # Set field size for visalization
        min_head_x = min(knots[0][0], min_head_x)
        min_head_y = min(knots[0][1], min_head_y)
        max_head_x = max(knots[0][0], max_head_x)
        max_head_y = max(knots[0][1], max_head_y)

# Visualize the snake on the field
width = 1 + max_head_x - min_head_x
height = 1 + max_head_y - min_head_y
field = [['.' for col in range(width)] for row in range(height)]

for tail_position in tail_positions:
    tail_x, tail_y = [int(s) for s in tail_position.split(':')]
    field[tail_y - min_head_y][tail_x - min_head_x] = '#'

for knot_index in range(9, -1, -1):
    knot_x = knots[knot_index][0]
    knot_y = knots[knot_index][1]
    character = 'H' if knot_index == 0 else str(knot_index)
    field[knot_y - min_head_y][knot_x - min_head_x] = character

for fieldline in field:
    print(''.join(fieldline))

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
