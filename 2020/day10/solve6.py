lines = open("2020/day10/data.txt").read().split('\n')
numbers = list(map(int, lines))
numbers += [0, max(numbers) + 3]
numbers.sort()

# Part 1
diffs = [numbers[n] - numbers[n - 1] for n in range(1, len(numbers))]
print('Answer1', diffs.count(1) * diffs.count(3))

# Part 2
scores = {}
numbers.reverse()
for key, number in enumerate(numbers):
    next_numbers = numbers[:key][-3:]

    if not next_numbers:
        scores[number] = 1
        continue

    scores[number] = 0
    for next_number in next_numbers:
        is_valid = next_number - number <= 3
        if is_valid:
            scores[number] += scores[next_number]
            # print('Count', scores[number], 'Next number', next_number)

print('Answer2', scores[0])