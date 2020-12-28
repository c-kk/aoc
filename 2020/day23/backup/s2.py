import copy

def pick_three_cups_clockwise_of_current(arrangement, current):
	current_index = arrangement.index(current)
	three_cups = []
	for i in range(1, 4):
		pick_index = (current_index + i) % len(arrangement)
		cup = arrangement[pick_index]
		three_cups.append(cup)
	for cup in three_cups:
		arrangement.remove(cup)
	print(f'{three_cups=}')
	return arrangement, three_cups

def select_destination_cup(arrangement, current):
	destination = current - 1
	while True:
		if destination < min(arrangement):
			destination = max(arrangement)
		is_not_picked_up = destination in arrangement
		if is_not_picked_up:
			break	
		destination -= 1
	print(f'{destination=}')
	return destination

def place_three_cups_clockwise_of_destination(arrangement, three_cups, destination):
	destination_index = arrangement.index(destination)
	for i, cup in enumerate(three_cups):
		arrangement.insert(destination_index + 1 + i, cup)
	# print(f'{arrangement=}')
	return arrangement

def select_new_current_cup(arrangement, current):
	current_index = arrangement.index(current)
	new_current_index = (current_index + 1) % len(arrangement)
	new_current = arrangement[new_current_index]
	# print(f'{new_current=}')
	return new_current

def make_solution_from_arrangement_part1(arrangement):
	solution = ''
	one_index = arrangement.index(1)
	length = len(arrangement)
	for i in range(1, length):
		index = (one_index + i) % length
		number = arrangement[index]
		solution += str(number)
	return solution

def make_solution_from_arrangement(arrangement):
	one_index = arrangement.index(1)
	index1 = (one_index + 1) % len(arrangement)
	index2 = (one_index + 2) % len(arrangement)
	number1 = arrangement[index1]
	number2 = arrangement[index2]
	solution = number1 * number2
	# print(f'{number1=} {number2=} {solution=}')
	return solution

arrangement1 = 198753462
arrangement2 = 389125467
arrangement = [int(d) for d in str(arrangement1)]
# arrangement += [number for number in range(10, 20 + 1)]
current = arrangement[0]

start_arrangement = copy.copy(arrangement)
start_solution = make_solution_from_arrangement(arrangement)
moves_with_start_solution = []
solutions = []

# for move in range(1, 10000001):
for move in range(1, 100 + 1):
	print(f'Move {move}')
	print(f'{current=}')
	print(f'{arrangement=}')

	solution = make_solution_from_arrangement(arrangement)
	solutions.append([move, copy.copy(arrangement), solution])
	if solution == start_solution:
		moves_with_start_solution.append(move)

	arrangement, three_cups = pick_three_cups_clockwise_of_current(arrangement, current)
	destination = select_destination_cup(arrangement, current)
	arrangement = place_three_cups_clockwise_of_destination(arrangement, three_cups, destination)
	current = select_new_current_cup(arrangement, current)
	print('')

print(f'{arrangement=}')
print(f'Part 1. Solution after {move} moves:', make_solution_from_arrangement_part1(arrangement))
print(f'Part 2. Solution after {move} moves:', make_solution_from_arrangement(arrangement))
# print(moves_with_start_solution)
# for solution in solutions:
# 	print(solution[1], solution[2])
# print('Expected solution after 10.000.000 moves: 149245887792')

# 149245887792 - too low
