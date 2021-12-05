nums = [69, 2, 3, 4, 8, 9, 10, 5, 7, 6] + list(range(11, 1000001)) + [1]

curr = 1
for move in range(10000000):
	x    = curr
	cups = []
	for _ in range(3):
		x     = nums[x]
		cups += [x]
	
	dest = curr - 1 or 1000000
	while dest in cups:
		dest = dest - 1 or 1000000
	
	nxt = nums[x]
	nums[x]    = nums[dest]
	nums[dest] = nums[curr]
	nums[curr] = nxt
	
	curr = nxt
	
num1 = nums[1]
num2 = nums[num1]
print(num1 * num2)