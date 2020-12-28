lines = open("d1.txt").read().split('\n')
lines = [int(line) for line in lines]
for line in lines: print(line)

for number1 in lines:
	for number2 in lines:
		summed = number1 + number2
		if summed == 2020:
			print('Number 1:', number1)
			print('Number 2:', number2)
			print('Multiply:', number1 * number2)
			exit()
