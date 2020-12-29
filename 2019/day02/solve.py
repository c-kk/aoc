def msg_start(mem, pos, *pars):
    opcode = mem[pos]
    pars_msg = ', '.join([f'{par:3}' for par in pars])
    msg = f'{pos:3}: opcode {opcode:2} [{pars_msg}]  '
    return msg

def do_ext(mem, pos):
    msg  = msg_start(mem, pos) + f'Exit, returning {mem[0]=}'
    return mem, pos + 1, msg

def do_add(mem, pos):
    par1, par2, par3 = mem[pos+1:pos+4]
    val1, val2 = mem[par1], mem[par2]
    mem[par3] = val1 + val2
    msg  = msg_start(mem, pos, par1, par2, par3)
    msg += f'Add {val1:7} + {val2:7}. Store at {par3:3}'
    return mem, pos + 4, msg
    
def do_mul(mem, pos):
    par1, par2, par3 = mem[pos+1:pos+4]
    val1, val2 = mem[par1], mem[par2]
    mem[par3] = val1 * val2
    msg  = msg_start(mem, pos, par1, par2, par3)
    msg += f'Mul {val1:7} * {val2:7}. Store at {par3:3}'
    return mem, pos + 4, msg

def run_and_debug_program(mem):
    return run_program(mem, debug=True)

def run_program(mem, debug=False):
    mem = mem.copy()
    pos = 0
    while True:
        opcode = mem[pos]
        if   opcode == 99: mem, pos, msg = do_ext(mem, pos)
        elif opcode == 1:  mem, pos, msg = do_add(mem, pos)
        elif opcode == 2:  mem, pos, msg = do_mul(mem, pos)
            
        if debug: print(msg)
        if opcode == 99: return mem[0]
            
mem = [int(s) for s in open("data.txt").read().split(',')]
mem[1] = 12
mem[2] = 2
print(mem)

result = run_and_debug_program(mem)
print('Answer 1:', result)

def find_noun_and_verb(wanted_result):    
    for noun in range(0, 100):
        for verb in range(0, 100):
            mem[1] = noun
            mem[2] = verb
            result = run_program(mem)
            if result == wanted_result:
                return 100 * noun + verb
           
print('Answer 2:', find_noun_and_verb(19690720))     