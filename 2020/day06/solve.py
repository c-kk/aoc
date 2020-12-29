lines = open("day6/data.txt").read().split('\n\n')

total = 0
for line in lines:
    sets = map(set, line.split('\n'))
    union = set.union(*sets)
    count = len(union)
    print(count, lines)
    total += count
print(total)

# total = 0
# for line in lines:
#     count = len(set(line) - {'\n'})
#     print(count, line)
#     total += count
# print(total)

# def count_unique_characters(line):
#     count = len(set(line) - {'\n'})
#     print(count, line)
#     return count
#
# total = sum(map(count_unique_characters, lines))
# print(total)