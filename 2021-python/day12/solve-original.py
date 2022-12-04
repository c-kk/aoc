# Solution from Reddit user 4HbQ
# Source: https://old.reddit.com/r/adventofcode/comments/rehj2r/2021_day_12_solutions/ho7x83o/

# Count explained
# A call to search(..., n) returns the number of valid paths from cave n to cave 'end'. 
# So if we want to know how many paths there are from the current cave to 'end',
# we simply add the counts of the adjacent caves.It's identical to this:
#
# count = 0
# for n in neighbours[cave]:
#     count += search(..., n)
# return count

from collections import defaultdict

lines = open("data.txt").read().split('\n')
neighbours = defaultdict(list)

for line in lines:
    a, b = line.strip().split('-')
    neighbours[a] += [b]
    neighbours[b] += [a]

def count(part, seen=[], cave='start'):
    if cave == 'end': return 1
    if cave in seen:
        if cave == 'start': return 0
        if cave.islower():
            if part == 1: return 0
            else: part = 1

    return sum(count(part, seen+[cave], n)
                for n in neighbours[cave])

print(count(part=1), count(part=2))
