import sys
import time

# Example usage: python3 s.py real2 100
file = sys.argv[0]
case = sys.argv[1]
movs = int(sys.argv[2])

# Define the cases: test-data and real-data for part 1 and part 2
test = [3,8,9,1,2,5,4,6,7]
real = [1,9,8,7,5,3,4,6,2]

if   case == 'test1': arra = test
elif case == 'test2': arra = test + [number for number in range(10, 1000001)]
elif case == 'real1': arra = real
elif case == 'real2': arra = real + [number for number in range(10, 1000001)]
print_links = case == 'test1' # Print the links on every step for testcase 1

# Convert array to links
links = {number: arra[(idx + 1) % len(arra)] for idx, number in enumerate(arra)}

# Start the calculation
curr = arra[0]
arra_max = max(arra)
stim = time.time()

for move in range(1, movs + 1):
	if print_links: print(f'{move:3}. {links}')

	# Pick cups
	cup1 = links[curr]
	cup2 = links[cup1]
	cup3 = links[cup2]
	nxt  = links[cup3]
	cups = [cup1, cup2, cup3]

	# Pick destination
	dest = curr - 1
	while True:
		if dest not in cups and dest >= 1:
			break
		else:
			if dest in cups: dest -= 1
			if dest < 1: dest = arra_max

	# Update links
	links[curr], links[dest], links[cup3] = links[cup3], cup1, links[dest]
	
	# Update current to next
	curr = nxt

# Measure the speed	
etim = time.time()
dtim = etim - stim # Delta
mtim = dtim / move # Time per move
tnee = 10000000 * mtim # Time needed for 10 million moves

# Create array from of links
curr = 1
arra = []
for i in links:
	arra.append(curr)
	curr = links[curr]

# Print the results
if print_links: print(f'Arra: {arra}')
print(f'Time per move:      {round(mtim, 6)}')
print(f'Time for 10M moves: {round(tnee, 1)} seconds')
print(f'Answer part 2:      {arra[1] * arra[2]}') # 693659135400 - correct!

if case == 'test1' and movs == 10:   assert arra == [1, 9, 2, 6, 5, 8, 3, 7, 4]
if case == 'test1' and movs == 1000: assert arra == [1, 8, 9, 2, 5, 6, 4, 7, 3]


