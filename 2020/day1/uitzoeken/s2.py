import itertools

numbers = [int(line) for line in open("d1.txt").read().split('\n')]

for combo in itertools.combinations(numbers, 2):
	if sum(combo) == 2020:
		print(combo[0] * combo[1])

for combo in itertools.combinations(numbers, 3):
	if sum(combo) == 2020:
		print(combo[0] * combo[1] * combo[2])

print([combo[0] * combo[1] for combo in itertools.combinations(numbers, 2) if sum(combo) == 2020])
print([combo[0] * combo[1] * combo[2] for combo in itertools.combinations(numbers, 3) if sum(combo) == 2020])