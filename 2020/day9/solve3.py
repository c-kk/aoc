import itertools

lines = open("2020/day9/data.txt").read().split('\n')
numbers = list(map(int, lines))
pre = 25

answer1 = None
for pointer in range(pre, len(numbers)):
    preamble = numbers[pointer - pre:pointer]
    target = numbers[pointer]
    if target not in map(sum, itertools.combinations(preamble, 2)):
        answer1 = numbers[pointer]

answer2 = None
for start in range(len(numbers)):
    for end in range(start + 2, len(numbers)):
        continious_range = numbers[start:end]
        if sum(continious_range) == answer1:
            answer2 = min(continious_range) + max(continious_range)

print(answer1)
print(answer2)
pass
