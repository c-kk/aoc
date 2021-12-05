import sys
import time
import game3 as game
import numpy as np

stim = time.time()

case = sys.argv[1]
movs = int(sys.argv[2])

test = [3,8,9,1,2,5,4,6,7]
real = [1,9,8,7,5,3,4,6,2]

if   case == 'test1': arra = test
elif case == 'test2': arra = test + [number for number in range(10, 1000001)]
elif case == 'real1': arra = real
elif case == 'real2': arra = real + [number for number in range(10, 1000001)]
print_arra = case == 'test1' and movs == 10

curr_idx = 0
leng = len(arra)

for move in range(1, movs + 1):
	curr = arra[curr_idx]
	if print_arra: print(f'{move:5}. {arra} at {curr}')
	
	# Pick cups
	if curr_idx <= leng - 4:
		sta = curr_idx + 1
		end = curr_idx + 4
		cups = arra[sta:end]
		del arra[sta:end]
		# arra = np.delete(arra, cups).tolist()
	else:
		cups = [arra[(curr_idx + i) % leng] for i in range(1, 4)]
		for cup in cups: arra.remove(cup)

	# Pick destination
	dest = curr - 1
	while True:
		try:
			dest_idx = arra.index(dest)
			break
		except:
			dest -= 1
			if dest < 1: dest = leng

	# Place cups
	sta = dest_idx + 1
	arra[sta:sta] = cups

	# Pick current	
	curr_idx = arra.index(curr)
	curr_idx = (curr_idx + 1) % leng

	# curr = game.pick_curr(arra, curr)
	# print(f'Moving {cups} to {dest}.')

etim = time.time()
dtim = etim - stim
mtim = dtim / move
tnee = 10000000 * mtim / 3600
print(f'Arra: {arra}')
print(f'Comm: p3 s5.py {case} {movs}')
print(f'Mtim: {round(mtim, 6)}')
print(f'Tnee: {round(tnee, 3)} hours')

if case == 'test1' and movs == 10:   assert arra == [5, 8, 3, 7, 4, 1, 9, 2, 6]
if case == 'test1' and movs == 1000: assert arra == [7, 3, 1, 8, 9, 2, 5, 6, 4]
