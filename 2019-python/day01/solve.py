lines = open("data.txt").read().split('\n')

# Part 1
total = 0
for mass in lines:
    fuel = int(mass) // 3 - 2  # divide by 3, round down, subtract 2
    total += fuel
print(total)

# Part 2
total = 0
for mass in lines:
    extra_mass = mass
    fuel = 0

    while True:
        extra_fuel_needed = int(extra_mass) // 3 - 2  # divide by 3, round down, subtract 2
        if extra_fuel_needed <= 0:
            break
        fuel += extra_fuel_needed
        extra_mass = extra_fuel_needed

    total += fuel
print(total)