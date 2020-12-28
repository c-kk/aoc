import itertools

lines = open("2020/day10/data.txt").read().split('\n')
numbers = list(map(int, lines))
numbers.append(0)
numbers.append(max(numbers) + 3)
numbers.sort()
diffs = [numbers[n] - numbers[n - 1] for n in range(1, len(numbers))]
answer1 = diffs.count(1) * diffs.count(3)
print(answer1)

pass
