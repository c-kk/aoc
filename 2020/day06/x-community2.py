groups = open("day6/data.txt").read().split('\n\n')

# Part one
print(sum(len(set.union(*map(set, g.split('\n')))) for g in groups))

# Part two
print(sum(len(set.intersection(*map(set, g.split('\n')))) for g in groups))
