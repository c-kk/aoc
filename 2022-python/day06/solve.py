line = open("data.txt").read()
print("Line:", line)

# Part 1
print("*** Part 1 ***")
score_part1 = 0

position = 4
while position <= len(line):
    characters = line[position - 4:position]
    print("Position", position, characters)

    all_characters_are_different = len(set(characters)) == len(characters)
    if (all_characters_are_different):
        print("Start-of-packet marker detected")
        score_part1 = position
        break

    position += 1

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

position = 14
while position <= len(line):
    characters = line[position - 14:position]
    print("Position", position, characters)

    all_characters_are_different = len(set(characters)) == len(characters)
    if (all_characters_are_different):
        print("Start-of-packet message detected")
        score_part2 = position
        break

    position += 1

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
