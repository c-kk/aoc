data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

for line in lines:        
    _, numbers = line.split(':')
    winning_numbers, numbers_you_have = numbers.split('|')
    winning_numbers = [int(number) for number in winning_numbers.split(' ') if number]
    numbers_you_have = [int(number) for number in numbers_you_have.split(' ') if number]

    matches = 0
    for number in numbers_you_have:
        if number in winning_numbers: matches += 1

    score = 2 ** (matches - 1)
    if score < 1: score = 0    
    score_part1 += score
    print(line, "matches", matches)

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0
line_counts = [1 for line in lines]
print(line_counts)

for line_index, line in enumerate(lines):        
    _, numbers = line.split(':')
    winning_numbers, numbers_you_have = numbers.split('|')
    winning_numbers = [int(number) for number in winning_numbers.split(' ') if number]
    numbers_you_have = [int(number) for number in numbers_you_have.split(' ') if number]

    matches = 0
    for number in numbers_you_have:
        if number in winning_numbers: matches += 1

    current_card_count = line_counts[line_index]
    for i in range(matches):
        line_counts[line_index + i + 1] += current_card_count

    print('line_index', line_index, line_counts)

for line_count in line_counts:
    score_part2 += line_count
    
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)