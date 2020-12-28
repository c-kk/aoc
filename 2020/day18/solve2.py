import collections
import math
import re
import sys

def calc(string):
	splitted = re.split("(\*|\+)", string) # Split by * and +, () = keep delimiters

	for opp in ['+', '*']:
		while opp in splitted:
			key = next(key for key, c in enumerate(splitted) if c == opp)
			num1 = int(splitted[key-1])
			num2 = int(splitted[key+1])

			if opp == '+':
				result = num1 + num2
			if opp == '*':
				result = num1 * num2
			splitted[key] = result
			[splitted.pop(k) for k in [key+1, key-1]]

	return splitted[0]

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')
lines = [line.replace(' ', '') for line in lines]
print(lines)

summed = 0

for line in lines:
	while True:
		right_bracket_index = line.find(")")
		if right_bracket_index != -1:
			left_bracket_index = line[:right_bracket_index].rfind("(")
			between_brackets = line[left_bracket_index+1:right_bracket_index]
			result = calc(between_brackets)
			line = line.replace(f"({between_brackets})", str(result))
		else:
			break
	
	summed += calc(line)
	print(line, summed)
print(summed)
# print(sum(lines))