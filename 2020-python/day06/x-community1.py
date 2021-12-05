day = open("day6/data.txt").read().split('\n\n')
print("Part 1:", sum(len(set(line)-{'\n'}) for line in day))
print("Part 2:", sum(len(set.intersection(*map(set, line.split("\n")))) for line in day))
