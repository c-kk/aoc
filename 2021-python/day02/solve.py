lines = open("data.txt").read().split('\n')
steps = [step.split(' ') for step in lines]

x = 0
z = 0

for [direction, amount] in steps:
    if direction == 'forward': x += int(amount)
    if direction == 'up': z -= int(amount)
    if direction == 'down': z += int(amount)

answer = x * z
print(answer)

x = 0
z = 0
aim = 0

for step in steps:
    direction = step[0]
    amount = int(step[1])

    if direction == 'up': aim -= amount
    if direction == 'down': aim += amount

    if direction == 'forward': 
        x += amount
        z += aim * amount

answer = x * z
print(answer)

# Short alternative for the first question
# lines = [[a, int(b)] for a,b in [l.split() for l in open("data.txt").read().split('\n')]]   

# x = sum([a for d,a in lines if d == 'forward'])
# z = sum([a if d == 'down' else -a if d == 'up' else 0 for d,a in lines])

# print(x*z)