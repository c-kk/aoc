lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")

# Split into tower lines, column count and move lines
tower_lines = list(filter(lambda line: not line.startswith("move"), lines))[:-2]
print("Tower lines:", tower_lines)

column_count_line = list(filter(lambda line: not line.startswith("move"), lines))[-2:-1][0]
column_count = int(column_count_line.split(' ')[-2])
print("Column count", column_count)

move_lines = list(filter(lambda line: line.startswith("move"), lines))
print("Move lines:", move_lines)

# Create columns
columns = []
for c in range(column_count):
    columns.append([])

for tower_line in tower_lines[::-1]:
    for index, column in enumerate(columns):
        value = tower_line[1+(index*4)]
        if value != ' ':
            column.append(value)

print("Columns (first = bottom):", columns)

# Execute moves
for move_line in move_lines:
    _, move_count, _, move_from, _, move_to = move_line.split(' ')
    move_count = int(move_count)
    move_from = int(move_from) - 1
    move_to = int(move_to) - 1

    for _ in range(move_count):
        item = columns[move_from].pop()
        columns[move_to].append(item)
        print("Move", item, "from column", move_from, "to column", move_to)
        print("Columns (first = bottom):", columns)

# Get message
message_part1 = ""
for column in columns:
    message_part1 += column[-1]
print("Message part 1:", message_part1)

# Part 2
print("*** Part 2 ***")

# Split into tower lines, column count and move lines
tower_lines = list(filter(lambda line: not line.startswith("move"), lines))[:-2]
print("Tower lines:", tower_lines)

column_count_line = list(filter(lambda line: not line.startswith("move"), lines))[-2:-1][0]
column_count = int(column_count_line.split(' ')[-2])
print("Column count", column_count)

move_lines = list(filter(lambda line: line.startswith("move"), lines))
print("Move lines:", move_lines)

# Create columns
columns = []
for c in range(column_count):
    columns.append([])

for tower_line in tower_lines[::-1]:
    for index, column in enumerate(columns):
        value = tower_line[1+(index*4)]
        if value != ' ':
            column.append(value)

print("Columns (first = bottom):", columns)

# Execute moves
for move_line in move_lines:
    _, move_count, _, move_from, _, move_to = move_line.split(' ')
    move_count = int(move_count)
    move_from = int(move_from) - 1
    move_to = int(move_to) - 1

    #items = columns[move_from][-move_count:]
    items = []
    for _ in range(move_count):
        item = columns[move_from].pop()
        items.insert(0, item)

    for item in items:
        columns[move_to].append(item)

    print("Move", items, "from column", move_from, "to column", move_to)
    #for _ in range(move_count):
    #    item = columns[move_from].pop()
    #    columns[move_to].append(item)
    #    
    #    print("Columns (first = bottom):", columns)

# Get message
message_part2 = ""
for column in columns:
    message_part2 += column[-1]
print("Message part 2:", message_part2)

print("*** Messages ***")
print("Message part 1:", message_part1)
print("Message part 2:", message_part2)
