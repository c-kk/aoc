import sys

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')
print(lines)

et = int(lines[0])
busses = set(lines[1].split(','))
busses.remove('x')
busses = [int(bus) for bus in busses]

remainders = {bus: (bus - et % bus) for bus in busses}
print(remainders)

id = min(remainders, key=remainders.get)
minutes = remainders[id]


print(id, minutes)
answer1 = id * minutes
print('Answer1', answer1)