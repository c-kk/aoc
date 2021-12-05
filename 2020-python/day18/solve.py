import collections
import math
import re
import sys

def split_and_keep_delimiters(delimiters, string, maxsplit=0):
    import re
    regex_pattern = '(' + '|'.join(map(re.escape, delimiters)) + ')'
    return re.split(regex_pattern, string, maxsplit)

def calc(string):
	splitted = split_and_keep_delimiters(['*', '+'], string)
	print(splitted)

	# ['8', '*', '3', '+', '9', '+', '3', '*', '4', '*', '3']
	result = int(splitted[0])
	for opp, number in zip(splitted[1::2],splitted[2::2]):
		if opp == '*':
			result *= int(number)
		if opp == '+':
			result += int(number)

	return result


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