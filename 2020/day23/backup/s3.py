import sys
import game

case = sys.argv[1]

if case == 'test1':
	arrangement = 389125467
	number_range = []
	move_range = range(1, 101)

elif case == 'real1':
	arrangement = 198753462 
	number_range = []
	move_range = range(1, 101)

elif case == 'test2':
	arrangement = 389125467
	number_range = range(10, 1000001)
	move_range = range(1, 10000001)

elif case == 'real2':
	arrangement = 198753462 
	number_range = range(10, 1000001)
	move_range = range(1, 10000001)

arrangement  = [int(d) for d in str(arrangement)] + [number for number in number_range]
current = arrangement[0]

for move in move_range:
	three_cups = game.pick_three_cups(arrangement, current)
	arangement = game.remove_three_cups(arrangement, three_cups)
	destination = game.pick_destination(arrangement, current)
	arrangement = game.place_three_cups(arrangement, three_cups, destination)
	current = game.pick_current(arrangement, current)
	print(f'Move {move}: moving {three_cups} to {destination}. Pointer is now at {current}')

print(f'\n== Finished ==')
print(f'Moves: {move}')
print(f'Case: {case}')
print(f'Numbers: {min(arrangement)} - {max(arrangement)}')
print(f'Final arrangement: {arrangement}')
print(f'Solution 1:', game.solution_string(arrangement))
print(f'Solution 2:', game.solution_multiply_two(arrangement))
# 149245887792 - too low
