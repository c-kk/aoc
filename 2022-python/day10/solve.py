lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

cycle = 1
x = 1
instr_index = 0
instr = None
params = None
finish_at = None

while True:
    # Finish running instructions
    if finish_at == cycle:
        if instr == 'addx':
            x += int(params[0])
        instr = None
        instr_index += 1

    # Start of cycle    
    print('cycle', str(cycle).ljust(3), 'x', str(x).ljust(3))

    # Start new instruction if needed
    if instr == None:        
        # Finish program if there are no more instructions
        if instr_index == len(lines):
            break

        # Get new instruction    
        instr, *params = lines[instr_index].split(' ')

        if instr == 'noop':
            finish_at = cycle + 1

        if instr == 'addx':
            finish_at = cycle + 2

        print('┗ instr', instr, params, 'finish_at', finish_at)

    # Check signal strength
    if cycle in [20,60,100,140,180,220]:
        signal_strength = cycle * x 
        score_part1 += signal_strength

    # Finish cycle
    cycle += 1

print("Score part 1:", score_part1)   

# Part 2
print("*** Part 2 ***")
cycle = 1
x = 1
instr_index = 0
instr = None
params = None
finish_at = None
crt_width = 40
crt_height = 6
crt = [['~' for col in range(crt_width)] for row in range(crt_height)]

while True:
    # Start of cycle    
    print('cycle', str(cycle).ljust(3), 'x', str(x).ljust(3))

    # Start new instruction if needed
    if instr == None:        
        # Get new instruction    
        instr, *params = lines[instr_index].split(' ')

        if instr == 'noop':
            finish_at = cycle + 0

        if instr == 'addx':
            finish_at = cycle + 1

        print('┗ instr', instr, params, 'finish_at', finish_at)

    # Set CRT pixel
    crt_pos = (cycle - 1) % (crt_width * crt_height)
    crt_row = crt_pos // crt_width
    crt_column = crt_pos % crt_width
    crt_character = '#' if x-1 <= crt_column <= x+1 else '.'
    crt[crt_row][crt_column] = crt_character
    print('┗ crt', crt_row, '-', crt_column, crt_character)

    # Draw CRT
    for crtline in crt:
        print(''.join(crtline))

    # Finish running instructions
    if finish_at == cycle:
        if instr == 'addx':
            x += int(params[0])
        instr = None
        instr_index += 1

        # Finish program if there are no more instructions
        if instr_index == len(lines):
            break

    cycle += 1

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:")
for crtline in crt:
    print(''.join(crtline))