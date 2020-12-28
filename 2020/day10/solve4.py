lines = open("2020/day10/data2.txt").read().split('\n')
numbers = list(map(int, lines))
numbers += [0, max(numbers) + 3]

# numbers = [0, 1, 2, 4, 5, 8]
numbers.sort()
numbers.reverse()

# Logic
# sol = {}
#
# sol[8] = {(8,)}                           # {(8,)}
# sol[5] = {(5, *c) for c in sol[8]}        # {(5, 8)}
# sol[4] = {(4, *c) for c in sol[5]}        # {(4, 5, 8)}
# sol[2] = {(2, *c) for c in sol[4]} | \
#          {(2, *c) for c in sol[5]}        # {(2, 5, 8), (2, 4, 5, 8)}
# sol[1] = {(1, *c) for c in sol[2]} | \
#          {(1, *c) for c in sol[4]}        # {(1, 4, 5, 8), (1, 2, 4, 5, 8), (1, 2, 5, 8)}
# sol[0] = {(0, *c) for c in sol[1]} | \
#          {(0, *c) for c in sol[2]}        # {(0, 2, 4, 5, 8), (0, 1, 2, 4, 5, 8), (0, 1, 2, 5, 8), (0, 1, 4, 5, 8), (0, 2, 5, 8)}

sol = {}
for key, number in enumerate(numbers):  # loop backwards
    next_numbers = numbers[:key][-3:]
    # print(number, next_numbers)

    if number in sol:
        continue

    if not next_numbers:
        sol[number] = {(number,)}
        continue

    sol[number] = set()

    for next_number in next_numbers:
        is_valid = next_number - number <= 3
        if is_valid:
            print(next_number)
            sol[number] = sol[number] | {(number, *c) for c in sol[next_number]}

    # print(len(sol), sol)
    # print(sol)
    # print(next_numbers)

# print('Solutions', sol[0])
print('Answer', len(sol[0]))
# print(sol[0])