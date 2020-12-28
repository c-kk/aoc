lines = open("day6/data.txt").read().split('\n\n')

total = 0
for line in lines:
    sets = map(set, line.split('\n'))
    intersect = set.intersection(*sets)
    count = len(intersect)
    print(count, lines)
    total += count
print(total)