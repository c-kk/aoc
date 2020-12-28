# mask = 100110X100000XX0X100X1100110X001X100
# mem[21836] = 68949
# mem[61020] = 7017251
# mask = X00X0011X11000X1010X0X0X110X0X011000
# mem[30885] = 231192
# mem[26930] = 133991367
# mem[1005] = 121034
# mem[20714] = 19917
# mem[55537] = 9402614

import sys

steps = open(f"data{sys.argv[1]}.txt").read().split('\nmask = ')
mem = {}

for step in steps:
	lines = step.split('\n')
	mask = lines[0].replace('mask = ', '')
	commands = [line[4:].split('] = ') for line in lines[1:]]
	for [key, value] in commands:
		key = int(key)
		binary = format(int(value), '036b')

		binary_result = "".join([binary[pos] if c == 'X' else c for pos, c in enumerate(mask)])
		result = int(binary_result, 2)

		mem[key] = result
		print(f"{key:5}, {value:8}, {binary_result}, {result}")

summed = sum(mem.values())
print(f"Answer1: {summed}")

# for pos, c in enumerate(mask):
# 	if c == 'X':
# 		r = binary[pos]
# 	else:
# 		r = c
# 	binary_result += r
# result = format(result, '036b')

# value2 = 13
# test = format((int(value), '036b')
# print(test)