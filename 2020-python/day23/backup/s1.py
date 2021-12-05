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
	return arrangement

def select_new_current_cup(arrangement, current):
	current_index = arrangement.index(current)
	new_current_index = (current_index + 1) % len(arrangement)
	new_current = arrangement[new_current_index]
	return new_current

def make_solution_from_arrangement(arrangement):
	solution = ''
	one_index = arrangement.index(1)
	length = len(arrangement)
	for i in range(1, length):
		index = (one_index + i) % length
		number = arrangement[index]
		solution += str(number)
	return solution

arrangement1 = 198753462
arrangement2 = 389125467
arrangement = [int(d) for d in str(arrangement1)]
current = arrangement[0]

for move in range(1, 101):
	arrangement, three_cups = pick_three_cups_clockwise_of_current(arrangement, current)
	destination = select_destination_cup(arrangement, current)
	arrangement = place_three_cups_clockwise_of_destination(arrangement, three_cups, destination)
	current = select_new_current_cup(arrangement, current)

print(f'{arrangement=}')
solution = make_solution_from_arrangement(arrangement)
print(f'Solution after {move} moves:', solution)