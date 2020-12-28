import copy

def pick_three_cups(arrangement, current):
	current_index = arrangement.index(current)
	three_cups = []
	for i in range(1, 4):
		pick_index = (current_index + i) % len(arrangement)
		cup = arrangement[pick_index]
		three_cups.append(cup)
	return three_cups

def remove_three_cups(arrangement, three_cups):
	for cup in three_cups:
		arrangement.remove(cup)
	return arrangement

def pick_destination(arrangement, current):
	destination = current - 1
	while True:
		if destination < min(arrangement):
			destination = max(arrangement)
		is_not_picked_up = destination in arrangement
		if is_not_picked_up:
			break	
		destination -= 1
	return destination

def place_three_cups(arrangement, three_cups, destination):
	destination_index = arrangement.index(destination)
	for i, cup in enumerate(three_cups):
		arrangement.insert(destination_index + 1 + i, cup)
	return arrangement

def pick_current(arrangement, current):
	current_index = arrangement.index(current)
	new_current_index = (current_index + 1) % len(arrangement)
	new_current = arrangement[new_current_index]
	return new_current

def solution_string(arrangement):
	solution = ''
	one_index = arrangement.index(1)
	length = len(arrangement)
	for i in range(1, length):
		index = (one_index + i) % length
		number = arrangement[index]
		solution += str(number)
	return solution

def solution_multiply_two(arrangement):
	one_index = arrangement.index(1)
	index1 = (one_index + 1) % len(arrangement)
	index2 = (one_index + 2) % len(arrangement)
	number1 = arrangement[index1]
	number2 = arrangement[index2]
	solution = number1 * number2
	return solution
