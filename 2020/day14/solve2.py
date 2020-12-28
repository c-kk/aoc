import sys

steps = open(f"data{sys.argv[1]}.txt").read().split('\nmask = ')
mem = {}

def get_results(results):
	new_results = []
	for result in results:
		x_pos = result.find('X')
		if x_pos:
			new_result = result[:x_pos] + "0" + result[x_pos + 1:]
			new_results.append(new_result)
			new_result = result[:x_pos] + "1" + result[x_pos + 1:]
			new_results.append(new_result)
	return new_results

for step in steps:
	lines = step.split('\n')
	mask = lines[0].replace('mask = ', '')
	commands = [line[4:].split('] = ') for line in lines[1:]]
	for [key, value] in commands:
		key = int(key)
		value = int(value)

		binary = format(key, '036b')
		binary_input = "0"

		for pos, m in enumerate(mask):
			if m == '0':
				r = binary[pos]
			elif m == '1':
				r = '1'
			elif m == 'X':
				r = 'X'
			binary_input += r

		keys = [binary_input]
		contains_x = True

		while contains_x:
			contains_x = False

			keys = get_results(keys)
			for key in keys:
				if 'X' in key:
					contains_x = True


		print(mask, mask.count('X'), len(keys))
		for key in keys:
			dec_key = int(key, 2)
			mem[dec_key] = value

# print(mem)
summed = sum(mem.values())
print(f"Answer2: {summed}")

