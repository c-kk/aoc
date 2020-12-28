numbers = [0, 0, 8, 15, 2, 12, 1, 4]

mem = {
	0: 1,
	1: 6,
	2: 4,
	8: 2,
	12: 5,
	15: 3,
}

number = 4
for key in range(7, 30000000 + 1):
	prev_key = mem.get(number, 0)
	mem[number] = key
	print(key)

	if prev_key == 0:
		number = 0
	else:
		number = key - prev_key


inv_mem = {v: k for k, v in mem.items()}
print(inv_mem[30000000])

