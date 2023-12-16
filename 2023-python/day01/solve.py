data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
    
# Part 1
print("*** Part 1 ***")

score_part1 = 0

for line in lines:
    print(line)

    numbers = []
    for index, char in enumerate(line):
        if char.isdigit():
            numbers.append(char)

    first_number = numbers[0]
    last_number = numbers[-1]
    combined_number = int(first_number + last_number)
    print(numbers, combined_number)

    score_part1 += combined_number

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

score_part2 = 0
wordnumbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

for line in lines:
    print(line)

    numbers = []
    for index, char in enumerate(line):
        if char.isdigit():
            numbers.append(char)
        else:
            part_of_line_that_is_left = line[index:]
            for wordnumber_index, wordnumber in enumerate(wordnumbers):
                realnumber = str(wordnumber_index + 1)
                if part_of_line_that_is_left.startswith(wordnumber):
                    numbers.append(realnumber)

    first_number = numbers[0]
    last_number = numbers[-1]
    combined_number = int(first_number + last_number)
    print(numbers, combined_number)

    score_part2 += combined_number

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)