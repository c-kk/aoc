groups = open("day6/data.txt").read().split('\n\n')

total = 0
for g in groups:
    lines = g.split('\n')
    sets = [set(line) for line in lines]
    union = set.union(*sets)
    count = len(union)
    # print(g, count)
    total += count
print(total)

total = 0
for g in groups:
    lines = g.split('\n')
    sets = [set(line) for line in lines]
    inter = set.intersection(*sets)
    count = len(inter)
    # print(g, count)
    total += count
print(total)

exit()
