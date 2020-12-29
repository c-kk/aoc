import itertools
import time

lines = open("data.txt").read().split('\n')
numbers = [int(number) for number in lines]

combos = list(itertools.combinations(numbers, 2))
for [num1, num2] in combos:
    if num1 + num2 == 2020:
        print(num1 * num2)

combos = list(itertools.combinations(numbers, 3))
for [num1, num2, num3] in combos:
    if num1 + num2 + num3 == 2020:
        print(num1 * num2 * num3)
