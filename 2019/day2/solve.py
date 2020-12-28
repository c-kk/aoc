code = [int(s) for s in open("2019/day2/data.txt").read().split(',')]
pointer = 0

code[1] = 12
code[2] = 2

while True:
    opcode = code[pointer]
    print("Pointer:", pointer, "Opcode:", opcode, "Code:", code[pointer:pointer+4])

    if opcode == 99:
        print('BRE:')
        break

    val1 = code[code[pointer + 1]]
    val2 = code[code[pointer + 2]]
    store_pos = code[pointer + 3]

    if opcode == 1:  # Add
        result = val1 + val2
        print('ADD:', val1, '+', val2, '=', result, 'storing in', store_pos)
        code[store_pos] = result

    elif opcode == 2:  # Multiply
        result = val1 * val2
        print('MUL:', val1, '*', val2, '=', result, 'storing in', store_pos)
        code[store_pos] = result

    pointer += 4  # Move forward 4 positions

print(code[0])
pass
