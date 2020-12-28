from functools import reduce

def intersect(set1, set2):
    return set1.intersection(set2)

sets = [
    {1, 2, 3, 4, 5},
    {2, 3, 4},
    {2, 4, 5},
]

in_all_sets = reduce(intersect, sets)
in_all_sets2 = sets[0].intersection(*sets[1:])

exit()

def add(num1, num2):
    return num1 + num2

lis = [1, 3, 5, 6, 2]
summed = reduce(add, lis)
print(summed)

max_value = reduce(lambda a, b: a if a > b else b, lis)
print(max_value)