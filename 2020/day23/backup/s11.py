# Normal list
import sys
import time

# Example usage: python3 s.py real2 100
file = sys.argv[0]
case = sys.argv[1]
movs = int(sys.argv[2])

stim = time.time()
test = [3,8,9,1,2,5,4,6,7]
real = [1,9,8,7,5,3,4,6,2]

if   case == 'test1': arra = test
elif case == 'test2': arra = test + [number for number in range(10, 1000001)]
elif case == 'real1': arra = real
elif case == 'real2': arra = real + [number for number in range(10, 1000001)]
print_arra = case == 'test1' and movs == 10

arra_max = max(arra)

for move in range(1, movs + 1):
	if print_arra: print(f'{move:5}. {arra}')

	# Pop first and append to end
	curr = arra.pop(0)
	arra.append(curr)

	# Pick cups
	cups = arra[0:3]
	del arra[0:3]	

	# Pick destination
	dest = curr - 1

	while True:
		try:
			dest_idx = arra.index(dest)
			break
		except:
			if dest in cups: dest -= 1
			if dest < 1: dest = arra_max

	# Place cups
	sta = dest_idx + 1
	arra[sta:sta] = cups

etim = time.time()
dtim = etim - stim
mtim = dtim / move
tnee = 10000000 * mtim / 3600
if print_arra: print(f'Arra: {arra}')
print(f'Comm: p3 {file} {case} {movs}')
print(f'Mtim: {round(mtim, 6)}')
print(f'Tnee: {round(tnee, 3)} hours')

if case == 'test1' and movs == 10:   assert arra == [8, 3, 7, 4, 1, 9, 2, 6, 5]
if case == 'test1' and movs == 1000: assert arra == [8, 9, 2, 5, 6, 4, 7, 3, 1]