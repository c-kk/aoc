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

busses = [(587, 550), (41, 14), (37, 0), (29, 21), (23, 9), (19, 1), (17, 0), (13, 10), (733, 665)]
# busses = [(629, 0), (587, 550), (41, 14), (29, 21), (23, 9), (19, 1), (13, 10), (733, 665)]
# busses = [(31, 25), (19, 12), (13, 12), (7, 0), (59, 55)]
# busses = [(7, 0), (13, 12)]
# busses = [(13, 12), (7, 0)]
# busses = [(7, 0), (13, 12), (59, 55)]

bus = busses.pop()
step = bus[0]
t = bus[1] - step

iterations = 0
for bus in busses:
	number, needed_remainder = bus

	while True:
		iterations += 1
		t += step

		actual_remainder = t % number
		difference = actual_remainder - needed_remainder
		is_correct = difference == 0

		print(f"{t:2d} % {number:2d} = {actual_remainder:2d} ({is_correct}, {needed_remainder}, {difference}) {iterations}")

		if is_correct:
			print("FOUND", t, "in", iterations)
			break

	step = step * number


# increment_per_step = number - step % number

# needed_steps = 0
# while difference != 0:
# 	if difference < 0:
# 		difference += number
# 		continue

# 	needed_steps += 1
# 	difference -= increment_per_step


# print(increment_per_step, needed_steps)	

# while True:
# 	found = True
# 	for bus in busses:
# 		iterations += 1
# 		number, needed_remainder = bus
# 		actual_remainder = t % number
# 		difference = actual_remainder - needed_remainder
# 		is_correct = difference == 0

# 		print(f"{t:2d} % {number:2d} = {actual_remainder:2d} ({is_correct}, {needed_remainder}, {difference}) {iterations}")
# 		if not is_correct:
# 			found = False
# 			break

# 	if found:
# 		print("FOUND", t, "in", iterations)
# 		break

# 	t += step



print(busses)
print([(bus[0], t % bus[0]) for bus in busses])

# 1068781
