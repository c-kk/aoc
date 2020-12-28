import fileinput
import itertools
from functools import reduce

numbers = [int(line) for line in fileinput.input()]
prod = lambda factors: reduce(lambda a, b: a * b, factors, 1)

for size in [2, 3]:
	print([prod(combo) for combo in itertools.combinations(numbers, size) if sum(combo) == 2020])