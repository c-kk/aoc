# Solution for AoC 2020 - Day 13
# 
# Example output of the script:
# Busses will arrive in {19: 11, 37: 23, 733: 150, 29: 20, 41: 40, 13: 11, 17: 7, 23: 11, 587: 5}
# Answer1: The first bus to arrive is 587 and will arrive in 5 minutes => 2935 
#
#               0 %  37 =   0
#             629 %  41 =  14
#          304029 % 587 = 550
#         4756424 %  13 =  10
#       108942467 %  19 =   1
#       768787406 %  23 =   9
#     96886200187 %  29 =  21
#  83278918745344 % 733 = 665
# 836024966345345 %  17 =   0
# Answer2: All busses will match their positions at time 836024966345345


lines = open(f"data{sys.argv[1]}.txt").read().split('\n')

current_time = int(lines[0])
busses = set(lines[1].split(','))
busses.remove('x')
busses = [int(bus) for bus in busses]
remainders = {bus: (bus - current_time % bus) for bus in busses}
first_bus = min(remainders, key=remainders.get)
time_to_wait = remainders[first_bus]

print(f"Busses will arrive in {remainders}")
print(f"Answer1: The first bus to arrive is {first_bus} and will arrive in {time_to_wait} minutes => {first_bus * time_to_wait} \n")


t = 0
step = 1
for key, bus in enumerate(lines[1].split(',')):
	if bus == 'x': continue

	bus = int(bus)
	needed_remainder = (bus - key) % bus

	while t % bus - needed_remainder != 0:
		t += step

	print(f"{t:15d} % {bus:3d} = {t % bus:3d}")
	step = step * bus

print(f"Answer2: All busses will match their positions at time {t}")
