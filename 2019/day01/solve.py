lines = open("2019/day1/data.txt").read().split('\n')

total = 0
for mass in lines:
    fuel = int(mass) // 3 - 2  # divide by 3, round down, subtract 2
    total += fuel
print(total)

pass

