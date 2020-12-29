lines = open("day6/data.txt").read().split('\n\n')

result1 = sum([len(set.union(*map(set, line.split('\n')))) for line in lines])
result2 = sum([len(set.intersection(*map(set, line.split('\n')))) for line in lines])

# result = sum([len(line) for line in lines])
# print(result)

exit()
