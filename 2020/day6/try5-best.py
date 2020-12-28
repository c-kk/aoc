groups = open("2020/day6/data.txt").read().split('\n\n')

total = 0
for g in groups:
    lines = g.split('\n')
    sets = [set(l) for l in lines]
    union = set.union(*sets)
    total += len(union)
print(total)

total = 0
for g in groups:
    lines = g.split('\n')
    sets = [set(l) for l in lines]
    intersection = set.intersection(*sets)
    total += len(intersection)
print(total)

pass