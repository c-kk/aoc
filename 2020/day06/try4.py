groups = open("day6/data.txt").read().split('\n\n')

total = 0
for g in groups:
    lines = g.split('\n')
    sets = [set(line) for line in lines]
    union = set.intersection(*sets)
    count = len(union)
    total += count
pass