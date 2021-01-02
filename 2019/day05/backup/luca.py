def get_value_by_mode(mem, instr, index):
    modes = [0, instr[0] // 100 % 10, instr[0] // 1000 % 10, instr[0] // 10000 % 10]
    return instr[index] if modes[index] else mem[instr[index]]

def add(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = value1 + value2
    mem[store] = result
    print(f'{pos}:{instr} Add {value1} + {value2}, store at {store}')
    return mem, nw_pos
    
def multiply(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = value1 * value2
    mem[store] = result
    print(f'{pos}:{instr} Multiply {value1} * {value2}, store at {store}')
    return mem, nw_pos

def store_input(mem, pos, inp):
    instr  = mem[pos:pos+2]
    store  = instr[1]
    nw_pos = pos + len(instr)
    value  = inp.pop(0)
    mem[store] = value
    print(f'{pos}:{instr} Store {inp} at {store}')
    return mem, nw_pos, inp

def output(mem, pos, out):
    instr  = mem[pos:pos+2]
    value  = get_value_by_mode(mem, instr, 1)
    nw_pos = pos + len(instr)
    out.append(value)
    print(f'{pos}:{instr} Output {value}')
    return mem, nw_pos, out

def jump_if_true(mem, pos):
    instr   = mem[pos:pos+3]
    value   = get_value_by_mode(mem, instr, 1)
    jump_to = get_value_by_mode(mem, instr, 2)
    nw_pos  = pos + len(instr)
    if value != 0: 
        nw_pos = jump_to
    print(f'{pos}:{instr} Jump to {jump_to} if {value} is not 0')
    return mem, nw_pos

def jump_if_false(mem, pos):
    instr   = mem[pos:pos+3]
    value   = get_value_by_mode(mem, instr, 1)
    jump_to = get_value_by_mode(mem, instr, 2)
    nw_pos  = pos + len(instr)
    if value == 0: 
        nw_pos = jump_to
    print(f'{pos}:{instr} Jump to {jump_to} if {value} is 0')
    return mem, nw_pos

def less_than(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = int(value1 < value2)
    mem[store] = result
    print(f'{pos}:{instr} {value1} < {value2}, store at {store}')
    return mem, nw_pos

def equals(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = int(value1 == value2)
    mem[store] = result
    print(f'{pos}:{instr} {value1} == {value2}, store at {store}')
    return mem, nw_pos

def run(mem, inp):
    print(f'## Run program ##')
    print(f'Mem {mem}')
    print(f'Inp {inp}')
    
    pos = 0
    out = []

    while True:
        opcode = mem[pos] % 100

        if opcode == 99: return out
        elif opcode == 1: mem, pos = add(mem, pos)
        elif opcode == 2: mem, pos = multiply(mem, pos)
        elif opcode == 3: mem, pos, inp = store_input(mem, pos, inp) 
        elif opcode == 4: mem, pos, out = output(mem, pos, out)   
        elif opcode == 5: mem, pos = jump_if_true(mem, pos) 
        elif opcode == 6: mem, pos = jump_if_false(mem, pos) 
        elif opcode == 7: mem, pos = less_than(mem, pos) 
        elif opcode == 8: mem, pos = equals(mem, pos) 
        else: raise Exception(f'Unknown opcode {opcode} at pos {pos} with mem {mem[pos:pos+4]}.')