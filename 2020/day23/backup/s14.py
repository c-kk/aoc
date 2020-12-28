# Numpy array
import sys
import time
import numpy as np

# Example usage: python3 s.py real2 100
file = sys.argv[0]
case = sys.argv[1]
movs = int(sys.argv[2])

test = [3,8,9,1,2,5,4,6,7]
real = [1,9,8,7,5,3,4,6,2]

test = np.array(test)
real = np.array(real)

if   case == 'test1': arra = test
elif case == 'test2': arra = np.concatenate((test, np.arange(10,1000001)))
elif case == 'real1': arra = real
elif case == 'real2': arra = np.concatenate((real, np.arange(10,1000001)))
print_arra = case == 'test1' and movs == 10

arra_max = max(arra)
curr_idx = 0
stim = time.time()

for move in range(1, movs + 1):
	if print_arra: print(f'{move:5}. {arra}')

	# Get first, append to end and increase current index with 1
	curr = arra[curr_idx]
	arra = np.append(arra, curr)
	curr_idx += 1

	# Pick cups
	sta = curr_idx + 0
	end = curr_idx + 3
	cups = arra[sta:end]
	curr_idx += 3

	# Pick destination
	dest = curr - 1

	while True:
		try:
			dest_idx = np.nonzero(arra == dest)[0][-1]
			break
		except:
			if dest in cups: dest -= 1
			if dest < 1: dest = arra_max

	# Place cups
	sta = dest_idx + 1
	arra = np.insert(arra, sta, cups)

arra = list(arra)
etim = time.time()
dtim = etim - stim
mtim = dtim / move
tnee = 10000000 * mtim / 3600
if print_arra: print(f'Arra: {arra}')
print(f'Comm: p3 {file} {case} {movs}')
print(f'Mtim: {round(mtim, 6)}')
print(f'Tnee: {round(tnee, 3)} hours')

if case == 'test1' and movs == 10:   
	assert arra == [8, 3, 7, 4, 1, 9, 2, 6, 5]
	print('Test ok')

if case == 'test1' and movs == 1000: 
	assert arra == [8, 9, 2, 5, 6, 4, 7, 3, 1]
	print('Test ok')
