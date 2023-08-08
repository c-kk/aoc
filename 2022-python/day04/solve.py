lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

for line in lines:
    print("Pair:", line)
    
    elf1, elf2 = line.split(',')
    print("Elf 1:", elf1)
    print("Elf 2:", elf2)
   
    elf1_low, elf1_high = elf1.split('-')
    elf2_low, elf2_high = elf2.split('-')

    elf1_low = int(elf1_low)
    elf1_high = int(elf1_high)
    elf2_low = int(elf2_low)
    elf2_high = int(elf2_high)

    elf1_fully_contains_elf2 = (elf1_low <= elf2_low) and (elf1_high >= elf2_high)
    print("Elf 1 fully contains Elf 2:", elf1_fully_contains_elf2)

    elf2_fully_contains_elf1 = (elf2_low <= elf1_low) and (elf2_high >= elf1_high)
    print("Elf 2 fully contains Elf 1:", elf2_fully_contains_elf1)

    if elf1_fully_contains_elf2 or elf2_fully_contains_elf1:
        score_part1 += 1
    
    print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

for line in lines:
    print("Pair:", line)
    
    elf1, elf2 = line.split(',')
    print("Elf 1:", elf1)
    print("Elf 2:", elf2)
   
    elf1_low, elf1_high = elf1.split('-')
    elf2_low, elf2_high = elf2.split('-')
    
    elf1_low = int(elf1_low)
    elf1_high = int(elf1_high)
    elf2_low = int(elf2_low)
    elf2_high = int(elf2_high)

    no_overlap_at_all = (elf1_low > elf2_high) or (elf2_low > elf1_high)
    elf1_and_elf2_overlap = not no_overlap_at_all

    print("Elf 1 and Elf 2 overlap:", elf1_and_elf2_overlap)

    if elf1_and_elf2_overlap:
        score_part2 += 1
    
    print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
