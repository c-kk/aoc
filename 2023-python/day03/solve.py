data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
width = len(lines[0])
height = len(lines)

# Part 1
print("*** Part 1 ***")
score_part1 = 0
current_number = ""
special_char_found = False
gears_found = []
gears_with_numbers = {}

for current_y, line in enumerate(lines):
    for current_x, char in enumerate(line):
        if char.isnumeric():
            current_number += char
            end_of_line_reached = current_x == len(line) - 1
            number_is_found = end_of_line_reached or not line[current_x + 1].isnumeric()

            for scan_y in range(current_y - 1, current_y + 2):
                for scan_x in range(current_x - 1, current_x + 2):
                    if scan_y > -1 and scan_y < height and scan_x > -1 and scan_x < width:
                        scan_char = lines[scan_y][scan_x]
                        if not scan_char.isnumeric() and scan_char != ".": special_char_found = True

            if number_is_found:
                print('YEAHHHH number found', int(current_number), special_char_found)
                if special_char_found:
                    score_part1 += int(current_number)
                current_number = ""
                special_char_found = False

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0
current_number = ""
gears_found = set()
gears_with_numbers = {}

for current_y, line in enumerate(lines):
    for current_x, char in enumerate(line):
        if char.isnumeric():
            current_number += char
            end_of_line_reached = current_x == len(line) - 1
            number_is_found = end_of_line_reached or not line[current_x + 1].isnumeric()
        
            for scan_y in range(current_y - 1, current_y + 2):
                for scan_x in range(current_x - 1, current_x + 2):
                    if scan_y > -1 and scan_y < height and scan_x > -1 and scan_x < width:
                        scan_char = lines[scan_y][scan_x]
                        if scan_char == "*": gears_found.add((scan_y, scan_x))

            if number_is_found:
                current_number = int(current_number)
                print('YEAHHHH number found', current_number, gears_found)
                if gears_found:
                    for gear_found in gears_found:
                        numbers_for_gear = gears_with_numbers.get(gear_found, set())
                        numbers_for_gear.add(current_number)
                        gears_with_numbers.update({gear_found: numbers_for_gear})
                current_number = ""
                gears_found = set()

for numbers in gears_with_numbers.values():
    if len(numbers) == 2:
        score_part2 += list(numbers)[0] * list(numbers)[1]

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)