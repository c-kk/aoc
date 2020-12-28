import sys

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')
# print(lines)

# et = int(lines[0])
# busses = set(lines[1].split(','))

busses = [[7, 0], [13, 1], [59, 4], [31, 6], [19, 7]]

current_bus = busses[0]
current_number = current_bus[0]

for next_bus in busses[1:]:
	t = 0
	next_number   = next_bus[0]
	minutes_later = next_bus[1]

	found = False
	while not found:
		found = t % next_number == next_number - minutes_later 
		print(t, current_number, next_number, minutes_later)
		if found:
			break
		t += current_number

	print("Found", t, current_number, next_number, minutes_later)
	current_number = t

print(t % 7, t % 13, t % 59, t % 31, t % 19)

# 1068781
# print(1068781 // 77)

# 23 * 38 % 97 == 1
# print(pow(38, -1, 97))


# multiple = 7 * 13 * 59 * 31 * 19
# print("multiple ", multiple)

# # added = 0 + 12 + 55 + 25 + 12
# # print(added)

# multiple2 = 7*0 + 13*12 + 59*55 + 31*25 + 19*12
# print("multiple2", multiple2)

# MMI = lambda A, n,s=1,t=0,N=0: (n < 2 and t%N or MMI(n, A%n, t, s-A//n*t, N or n),-1)[n<1]
# mmi = MMI(multiple, multiple2)
# print("mmi      ", mmi)

# 1068781


# Try 2
# t = 1
# found = False
# while not found:
# 	found = t % 7 == 0 and \
# 		    t % 13 == 13 - 1
# 	print(t)
# 	t += 1

# # 77, want
# # 77 / 7  = 11, 0 over
# # 77 / 13 =  5, 12 over

# multiple = 7 * 13
# print("multiple ", multiple)

# multiple2 = 7*0 + 13*12
# print("multiple2", multiple2)

# mmi = MMI(2, 156)
# print(1068781 / 7)

