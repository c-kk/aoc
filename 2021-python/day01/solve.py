import itertools
import time

lines = open("data.txt").read().split('\n')
numbers = [int(number) for number in lines]

increases = 0
previous_num = 1000

for num in numbers:
    if num > previous_num:
        increases = increases + 1
    previous_num = num

print(increases)

increases = 0
prev_1 = 1000
prev_2 = 1000
prev_3 = 1000

for num in numbers:
    if (prev_1 + prev_2 + prev_3) < (prev_2 + prev_3 + num):
        increases = increases + 1
    prev_1 = prev_2
    prev_2 = prev_3
    prev_3 = num    

print(increases)