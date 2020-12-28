import sys
import re
import collections
import math
import itertools

result = 0
lines = open(f"d{sys.argv[1]}.txt").read().split('\n')
lines = [int(line) for line in lines]
print(lines)

combos = itertools.combinations(lines, 2)
for combo in combos:
	summed = combo[0] + combo[1]
	if summed == 2020:
		result = combo[0] * combo[1]

print(result)

combos = itertools.combinations(lines, 3)
for combo in combos:
	summed = combo[0] + combo[1] + combo[2]
	if summed == 2020:
		result = combo[0] * combo[1] * combo[2]

print(result)