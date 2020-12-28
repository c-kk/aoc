lines = open("2020/day10/data.txt").read().split('\n')
numbers = list(map(int, lines))
numbers += [0, max(numbers) + 3]

# numbers = [0, 1, 2, 4, 5, 8]
numbers.sort()
numbers.reverse()

# Logic
sol = {}

sol[8] = 1                        # {(8,)}
sol[5] = sol[8]                   # {(5, 8)}
sol[4] = sol[5]                   # {(4, 5, 8)}
sol[2] = sol[4] + sol[5]          # {(2, 5, 8), (2, 4, 5, 8)}
sol[1] = sol[2] + sol[4]          # {(1, 4, 5, 8), (1, 2, 4, 5, 8), (1, 2, 5, 8)}
sol[0] = sol[1] + sol[2]          # {(0, 2, 4, 5, 8), (0, 1, 2, 4, 5, 8), (0, 1, 2, 5, 8), (0, 1, 4, 5, 8), (0, 2, 5, 8)}

sol = {}
for key, number in enumerate(numbers):  # loop backwards
    next_numbers = numbers[:key][-3:]

    if not next_numbers:
        sol[number] = 1
        continue

    sol[number] = 0

    for next_number in next_numbers:
        is_valid = next_number - number <= 3
        if is_valid:
            sol[number] += sol[next_number]
            print('Count', sol[number], 'Next number', next_number)

print('Answer', sol[0])