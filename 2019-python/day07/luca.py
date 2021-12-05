import attr

@attr.s
class Program:
    mem = attr.ib() # Memory
    des = attr.ib(default=None)  # Description of the program
    inp = attr.ib(default=attr.Factory(list))  # Input buffer
    out = attr.ib(default=attr.Factory(list))  # Output buffer
    pos = attr.ib(default=0)  # Position of the pointer
    reb = attr.ib(default=0)  # Relative base for relative mode parameters
    opc = attr.ib(default=None)  # Last opcode at exit


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def print_mem(mem):
    print('├ mem      0     1     2     3     4     5     6     7     8     9')
    print('     ┌    ──    ──    ──    ──    ──    ──    ──    ──    ──    ──')
    index = 0
    for row in list(chunks(mem, 10)):
        print(f'{index:5}|', end=' ')
        for item in row:
            print(f'{item:5}', end=' ')
            index += 1
        print()

def print_instr(pos, instr, msg2, msg3):
    msg1 = f'{pos:5}: '
    for item in instr: msg1 += f'{item:5}'
    total = f'{msg1:28} {msg2:20} {msg3}'
    print(total)
        
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
    print_instr(pos, instr, f'ADD {value1} + {value2}.', f'Store {result} at {store}')
    return mem, nw_pos
    
def multiply(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = value1 * value2
    mem[store] = result
    print_instr(pos, instr, f'MUL {value1} * {value2}.', f'Store {result} at {store}')
    return mem, nw_pos

def store_input(mem, pos, inp):
    instr  = mem[pos:pos+2]
    store  = instr[1]
    nw_pos = pos + len(instr)
    value  = inp.pop(0)
    mem[store] = value
    print_instr(pos, instr, f'STO Input {value}.', f'Store {value} at {store}')
    return mem, nw_pos, inp

def output(mem, pos, out):
    instr  = mem[pos:pos+2]
    value  = get_value_by_mode(mem, instr, 1)
    nw_pos = pos + len(instr)
    out.append(value)
    print_instr(pos, instr, f'OUT Mem {value}.', f'Store {value} at output {len(out)-1}')
    return mem, nw_pos, out

def jump_if_true(mem, pos):
    instr   = mem[pos:pos+3]
    value   = get_value_by_mode(mem, instr, 1)
    jump_to = get_value_by_mode(mem, instr, 2)
    nw_pos  = pos + len(instr)
    if value != 0: 
        nw_pos = jump_to
        msg = f'Jump to {jump_to}'
    else:
        msg = 'No jump'
    print_instr(pos, instr, f'JTR Compare {value} != 0.', msg)
    return mem, nw_pos

def jump_if_false(mem, pos):
    instr   = mem[pos:pos+3]
    value   = get_value_by_mode(mem, instr, 1)
    jump_to = get_value_by_mode(mem, instr, 2)
    nw_pos  = pos + len(instr)
    if value == 0: 
        nw_pos = jump_to
        msg = f'Jump to {jump_to}'
    else:
        msg = 'No jump'
    print_instr(pos, instr, f'JFA Compare {value} == 0.', msg)
    return mem, nw_pos

def less_than(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = int(value1 < value2)
    mem[store] = result
    print_instr(pos, instr, f'LES Compare {value1} < {value2}.', f'Store {result} at {store}')
    return mem, nw_pos

def equals(mem, pos):
    instr  = mem[pos:pos+4]
    value1 = get_value_by_mode(mem, instr, 1)
    value2 = get_value_by_mode(mem, instr, 2)
    store  = instr[3]
    nw_pos = pos + len(instr)
    result = int(value1 == value2)
    mem[store] = result
    print_instr(pos, instr, f'EQU Compare {value1} == {value2}.', f'Store {result} at {store}')
    return mem, nw_pos

def run(program: Program):
    mem = program.mem
    des = program.des
    inp = program.inp
    out = program.out
    pos = program.pos
    reb = program.reb

    print('Run Luca program')
    print(f'├ {des}')
    print(f'├ inp {inp}')
    print(f'├ pos {pos}')
    print_mem(mem)
    print(f'├ steps') 

    while True:
        opc = mem[pos] % 100

        needs_input = opc == 3 and len(inp) == 0
        if opc == 99 or needs_input: 
            print(f'├ opc {opc}')
            print(f'├ out {out}\n')
            return Program(mem, des, inp, out, pos, reb, opc)

        elif opc == 1: mem, pos = add(mem, pos)
        elif opc == 2: mem, pos = multiply(mem, pos)
        elif opc == 3: mem, pos, inp = store_input(mem, pos, inp) 
        elif opc == 4: mem, pos, out = output(mem, pos, out)   
        elif opc == 5: mem, pos = jump_if_true(mem, pos) 
        elif opc == 6: mem, pos = jump_if_false(mem, pos) 
        elif opc == 7: mem, pos = less_than(mem, pos) 
        elif opc == 8: mem, pos = equals(mem, pos) 
        else: raise Exception(f'Unknown opcode {opc} at pos {pos} with mem {mem[pos:pos+4]}.')