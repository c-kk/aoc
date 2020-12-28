def run_code(noun, verb):
    memory = [int(s) for s in open("2019/day2/data.txt").read().split(',')]
    pointer = 0
    memory[1] = noun
    memory[2] = verb

    while True:
        opcode = memory[pointer]
        # print("Pointer:", pointer, "Opcode:", opcode, "Code:", code[pointer:pointer+4])

        if opcode == 1:  # Add
            [val1, val2, val3] = [memory[pointer + i] for i in [1, 2, 3]]
            result = memory[val1] + memory[val2]
            memory[val3] = result
            pointer += 4
            # print('ADD:', val1, '+', val2, '=', result, 'storing in', store_pos)

        elif opcode == 2:  # Multiply
            [val1, val2, val3] = [memory[pointer + i] for i in [1, 2, 3]]
            result = memory[val1] * memory[val2]
            memory[val3] = result
            pointer += 4
            # print('MUL:', val1, '*', val2, '=', result, 'storing in', store_pos)

        if opcode == 99:
            # print('BRE:')
            break

    result = memory[0]
    return result

noun = 12
verb = 2

for noun in range(0, 99):
    for verb in range(0, 99):
        result = run_code(noun, verb)
        print(noun, verb, result)
        if result == 19690720:
            print(100 * noun + verb)
            exit()
pass
