lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0
for line in lines:
    # Divide the items between the two compartments in the rucksack
    item_count = len(line)
    compartment1 = line[0:item_count//2]
    compartment2 = line[item_count//2:]
    print("Rucksack:", line)
    print("Compartment 1:", compartment1)
    print("Compartment 2:", compartment2)

    # Find the matching item
    match = ""
    for item in compartment1:
        if item in compartment2:
            match = item
            print("Match:", match)
            break 

    # Calculate the priority of the matching item    
    ascii_code = ord(match)

    if ascii_code >= 97: # a-z
        priority = ascii_code - 96
    else: # A-Z
        priority = ascii_code - 38

    print("Priority:", priority)

    # Add the priority to the score
    score_part1 += priority
    print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0
for rucksack1, rucksack2, rucksack3 in zip(*[iter(lines)]*3):
    print("Rucksack 1:", rucksack1)
    print("Rucksack 2:", rucksack2)
    print("Rucksack 3:", rucksack3)

    # Find the matching item
    match = ""
    for item in rucksack1:
        if (item in rucksack2) and (item in rucksack3):
            match = item
            print("Match:", match)
            break 

    # Calculate the priority of the matching item    
    ascii_code = ord(match)

    if ascii_code >= 97: # a-z
        priority = ascii_code - 96
    else: # A-Z
        priority = ascii_code - 38

    print("Priority:", priority)

    # Add the priority to the score
    score_part2 += priority
    print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
