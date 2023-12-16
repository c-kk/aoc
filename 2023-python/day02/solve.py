data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
    
# Part 1
print("*** Part 1 ***")
score_part1 = 0

for line_index, line in enumerate(lines):
    succes = True
    interesting_stuff = line.split(": ",1)[1]
    grabs = interesting_stuff.replace('; ', ', ').split(', ')

    for grab in grabs:
        [amount, color] = grab.split(' ')
        amount = int(amount)
        if color == 'blue' and amount > 14: succes = False
        elif color == 'green' and amount > 13: succes = False
        elif color == 'red' and amount > 12: succes = False

    score_part1 += (line_index + 1) * succes
    print(succes, interesting_stuff)


print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

for line in lines:
    min_blue = 0
    min_green = 0
    min_red = 0

    interesting_stuff = line.split(": ",1)[1]
    grabs = interesting_stuff.replace('; ', ', ').split(', ')

    for grab in grabs:
        [amount, color] = grab.split(' ')
        amount = int(amount)
        if color == 'blue': min_blue = max(min_blue, amount)
        if color == 'green': min_green = max(min_green, amount)
        if color == 'red': min_red = max(min_red, amount)

    megalucky = min_blue * min_green * min_red

    score_part2 += megalucky
    print(megalucky, interesting_stuff, min_blue, min_green, min_red)

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)