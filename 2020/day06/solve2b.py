lines = open("day6/data.txt").read().split('\n\n')

def count_overlapping_characters(line):
    sets = map(set, line.split('\n'))
    intersect = set.intersection(*sets)
    count = len(intersect)
    print(count, line)
    return count

total = sum(map(count_overlapping_characters, lines))
print(total)