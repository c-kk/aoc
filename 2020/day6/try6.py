groups = open("day6/data.txt").read().split('\n\n')

total1 = sum([len(set.union(*[set(line) for line in g.split('\n')])) for g in groups])
total2 = sum([len(set.intersection(*[set(line) for line in g.split('\n')])) for g in groups])

pass