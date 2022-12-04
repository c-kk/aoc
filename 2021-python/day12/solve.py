# Solution from Reddit user 4HbQ
# Source: https://old.reddit.com/r/adventofcode/comments/rehj2r/2021_day_12_solutions/ho7x83o/

# Rewrite of the original version (see solve-original.py) 
# to only use functions that also exists in Golang.
# To goal is to use the same logic in the Go version of the solution.

lines = open("data.txt").read().split('\n')
neighbours = {}

for line in lines:
    a, b = line.strip().split('-')

    if a not in neighbours:
        neighbours[a] = []

    if b not in neighbours:
        neighbours[b] = []

    neighbours[a] += [b]
    neighbours[b] += [a]

def count(cave, seen, allowDoubleVisit):
    if cave == 'end': 
        return 1

    if cave in seen:
        if cave == 'start': 
            return 0
        
        if ord(cave[0]) > 90:
            if not allowDoubleVisit:
                return 0
            else:
                allowDoubleVisit=False
    
    total = 0
    for neighbour in neighbours[cave]:
        seen = seen + [cave]
        pathCount = count(neighbour, seen, allowDoubleVisit)
        total += pathCount
    return total

seen=[] 
cave='start'
allowDoubleVisit=False
print(count(cave, seen, allowDoubleVisit))

seen=[] 
cave='start'
allowDoubleVisit=True
print(count(cave, seen, allowDoubleVisit))
