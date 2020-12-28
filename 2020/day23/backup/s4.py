import sys
import game
import hist

case = sys.argv[1]
test = 389125467
real = 198753462
if case == 'test1':
	arrangement = test
	number_range = []
	max_move = 100
elif case == 'real1':
	arrangement = real
	number_range = []
	max_move = 100
elif case == 'test2':
	arrangement = test
	number_range = range(10, 1000001)
	max_move = 10000000
elif case == 'real2':
	arrangement = real
	number_range = range(10, 1000001)
	max_move = 10000000
elif case == 'test3':
	arrangement = test
	number_range = []
	max_move = 15
elif case == 'test4':
	arrangement = test
	number_range = []
	max_move = 100000
elif case == 'real4':
	arrangement = real
	number_range = []
	max_move = 100000
elif case == 'test5':
	arrangement = test
	number_range = range(10, 101)
	max_move = 100
elif case == 'real5':
	arrangement = real
	number_range = range(10, 101)
	max_move = 100

arrangement = [int(d) for d in str(arrangement)] + [number for number in number_range]
current = arrangement[0]
history = dict()

for move in range(1, max_move + 1):
	last_seen_at = hist.last_seen_at(history, arrangement)	
	history = hist.add_to_history(history, arrangement, move)
	print(f'{move:3}. {arrangement} at {current}.', end=' ')
	# print(f'{move:3}. At {current}.', end=' ')
	if last_seen_at: print(f'Loop length: {move - last_seen_at}.', end=' ')

	three_cups = game.pick_three_cups(arrangement, current)
	arangement = game.remove_three_cups(arrangement, three_cups)
	destination = game.pick_destination(arrangement, current)
	arrangement = game.place_three_cups(arrangement, three_cups, destination)
	current = game.pick_current(arrangement, current)
	print(f'Moving {three_cups} to {destination}.')

print(f'\n== Finished ==')
print(f'Moves: {move}')
print(f'Case: {case}')
print(f'Numbers: {min(arrangement)} - {max(arrangement)}')
print(f'Final arrangement: {arrangement}')
print(f'Solution 1:', game.solution_string(arrangement))
print(f'Solution 2:', game.solution_multiply_two(arrangement))
# 149245887792 - too low
