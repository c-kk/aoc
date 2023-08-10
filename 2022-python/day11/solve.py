import math

lines = open("data.txt").read().split('\n')

# Convert lines
items = [[int(item) for item in items] for items in [itemline[18:].split(', ') for itemline in lines[1::7]]]
operations = [[item for item in items] for items in [itemline[23:].split(' ') for itemline in lines[2::7]]]
tests = [int(itemline[21:]) for itemline in lines[3::7]]
true_monkeys = [int(itemline[29:]) for itemline in lines[4::7]]
false_monkeys = [int(itemline[29:]) for itemline in lines[5::7]]
monkey_count = len(items)
# print(monkey_count, items, operations, tests, true_monkeys, false_monkeys)

# Part 1
print("*** Part 1 ***")
round = 1
inspections = [0 for monkey in range(monkey_count)]

while round <= 20:
    for monkey in range(monkey_count):

        # Inspect and distribute items
        while len(items[monkey]) > 0:
            # Increase inspection count
            inspections[monkey] += 1

            # Pop item
            old = items[monkey].pop(0)

            # Apply operation
            operator, value = operations[monkey]

            if operator == '+':
                if value == 'old':
                    new = old + old
                else:
                    new = old + int(value)
            else:
                if value == 'old':
                    new = old * old
                else:
                    new = old * int(value)
            
            # Decreasy worry
            new = math.floor(new / 3)

            # Do test
            divisor = tests[monkey]
            is_divisible = new % divisor == 0

            # Distribute item by test result
            if is_divisible:
                true_monkey = true_monkeys[monkey]
                items[true_monkey].append(new)
            else:
                false_monkey = false_monkeys[monkey]
                items[false_monkey].append(new)
    
    print('Round', round, 'items', items, 'inspections', inspections)
    round += 1

# Calculate monkey factor
inspections.sort()
highest = inspections[-1]
second_highest = inspections[-2]
score_part1 = highest * second_highest
print("Score part 1:", score_part1)   

# Part 2
print("*** Part 2 ***")
round = 1
inspections = [0 for monkey in range(monkey_count)]
items = [[int(item) for item in items] for items in [itemline[18:].split(', ') for itemline in lines[1::7]]]
prime_multiple = math.prod(tests)

while round <= 10000:
    for monkey in range(monkey_count):

        # Inspect and distribute items
        while len(items[monkey]) > 0:
            # Increase inspection count
            inspections[monkey] += 1

            # Pop item
            old = items[monkey].pop(0)

            # Apply operation
            operator, value = operations[monkey]

            if operator == '+':
                if value == 'old':
                    new = old * 2
                else:
                    new = old + int(value)
            else:
                if value == 'old':
                    new = old * old
                else:
                    new = old * int(value)

            new = new

            # Do test
            divisor = tests[monkey]
            quotient = new % divisor
            remainder = new % divisor 
            is_divisible = remainder == 0

            # Reduce size of item by dividing it by all primes in the tests
            new = new % prime_multiple

            # Distribute item by test result
            if is_divisible:
                true_monkey = true_monkeys[monkey]
                items[true_monkey].append(new)
            else:
                false_monkey = false_monkeys[monkey]
                items[false_monkey].append(new)
    
    print('Round', round, 'items', items, 'inspections', inspections)
    round += 1

# Calculate monkey factor
inspections.sort()
highest = inspections[-1]
second_highest = inspections[-2]
score_part2 = highest * second_highest
print("Score part 2:", score_part2) 

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
