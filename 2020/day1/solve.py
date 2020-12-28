import itertools

numbers = []

with open('data.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()

    for line in filecontents:
        number = int(line[:-1])
        numbers.append(number)


combos = list(itertools.combinations(numbers, 2))
print(combos)

for combo in combos:
    number1 = combo[0]
    number2 = combo[1]
    total = number1 + number2

    if total == 2020:
        multiple = number1 * number2
        print(number1, number2, multiple)


combos = list(itertools.combinations(numbers, 3))
#print(combos)

for combo in combos:
    number1 = combo[0]
    number2 = combo[1]
    number3 = combo[2]
    total = number1 + number2 + number3

    if total == 2020:
        multiple = number1 * number2 * number3
        print(number1, number2, number3, multiple)
