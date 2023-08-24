data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')

# Part 1
print("*** Part 1 ***")

exit()
score_part1 = 0
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

score_part2 = 0
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)