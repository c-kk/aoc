import sys
import time

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')
inputs = lines[1].split(',')
# print(inputs)

busses = []
for key, input in enumerate(inputs):
	if input == 'x':
		continue
	number = int(input)
	remainder = (number - key) % number
	bus = (number, remainder)
	busses.append(bus)

# busses = [(587, 550), (41, 14), (37, 0), (29, 21), (23, 9), (19, 1), (17, 0), (13, 10), (733, 665)]
# busses = [(629, 0), (587, 550), (41, 14), (29, 21), (23, 9), (19, 1), (13, 10), (733, 665)]
# busses = [(31, 25), (19, 12), (13, 12), (7, 0), (59, 55)]
busses = [(7, 0), (13, 12)]
# busses = [(13, 12), (7, 0)]
# busses = [(7, 0), (13, 12), (59, 55)]

bus = busses.pop()
step = bus[0]
t = bus[1]

iterations = 0
while True:
	found = True
	for bus in busses:
		iterations += 1
		number, needed_remainder = bus
		actual_remainder = t % number
		difference = actual_remainder - needed_remainder
		# while difference < 0:
		# 	difference += number
		is_correct = difference == 0

		print(f"{t:2d} % {number:2d} = {actual_remainder:2d} ({is_correct}, {needed_remainder}, {difference}) {iterations}")
		if not is_correct:
			found = False
			increment_per_step = number - step % number

			needed_steps = 0
			while difference != 0:
				if difference < 0:
					difference += number
					continue

				needed_steps += 1
				difference -= increment_per_step


			print(increment_per_step, needed_steps)	
			break

	if found:
		print("FOUND", t, "in", iterations)
		# print(t)
		# iterations = 0
		break

	t += needed_steps * step




print(busses)

print([(bus[0], t % bus[0]) for bus in busses])

# print(t % 7, 13 - t % 13, 59 - t % 59, 31 - t % 31, 19 - t % 19)

# 1068781
