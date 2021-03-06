import attr

@attr.s
class Program:
    mem = attr.ib() # Memory
    des = attr.ib(default=None)  # Description of the program
    inp = attr.ib(default=attr.Factory(list))  # Input buffer
    out = attr.ib(default=attr.Factory(list))  # Output buffer
    pos = attr.ib(default=0)  # Position of the pointer
    rba = attr.ib(default=0)  # Relative base for relative mode parameters
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

def get_value(mem, pm, rba, mode):
    if mode == 0: # Positional mode 
        pass

    elif mode == 1: # Immediate mode 
        return pm
  
    elif mode == 2: # Relative mode 
        pm += rba

    try:
        return mem[pm]
    except:
        if pm >= len(mem): return 0

def store_value(mem, pm, rba, mode, value):
    if mode == 0: # Positional mode
        pass
   
    elif mode == 2: # Relative mode      
        pm += rba

    elif mode == 1: # Immediate mode
        raise Exception('Immediate mode not allowed for storing parameters')

    try:
        mem[pm] = value
    except:
        # Extend memory if pos is higher than or equal to the memory length
        if pm >= len(mem):
            mem.extend([0] * (pm - len(mem) + 1))
            mem[pm] = value

    return mem, pm    

def create_run(**params):
    return run(Program(**params))

def run(program: Program, debug=True):
    mem = program.mem
    des = program.des
    inp = program.inp
    out = program.out
    pos = program.pos
    rba = program.rba
    dbg = debug

    if dbg:
        print('Run Luca program')
        print(f'├ {des}')
        print(f'├ inp {inp}')
        print(f'├ pos {pos}')
        print_mem(mem)
        print(f'├ steps') 

    while True:
        opcm = mem[pos]
        md3, rm3 = opcm // 10000, opcm % 10000
        md2, rm2 = rm3 // 1000, rm3 % 1000
        md1, opc = rm2 // 100, rm2 % 100

        if opc == 1: 
            nw_pos = pos + 4
            [pm1, pm2, pm3] = mem[pos+1:nw_pos]
            value1 = get_value(mem, pm1, rba, md1)
            value2 = get_value(mem, pm2, rba, md2)
            result = value1 + value2
            mem, store = store_value(mem, pm3, rba, md3, result)
            if dbg: print_instr(pos, [pm1, pm2, pm3], f'ADD {value1} + {value2}.', f'Store {result} at {store}')

        elif opc == 2:
            nw_pos = pos + 4
            [pm1, pm2, pm3] = mem[pos+1:nw_pos]
            value1 = get_value(mem, pm1, rba, md1)
            value2 = get_value(mem, pm2, rba, md2)
            result = value1 * value2
            mem, store = store_value(mem, pm3, rba, md3, result)
            if dbg: print_instr(pos, [pm1, pm2, pm3], f'MUL {value1} * {value2}.', f'Store {result} at {store}')

        elif opc == 3: 
            if len(inp) == 0:
                if dbg:
                    print(f'{pos:5}: {opc:5}')
                    print(f'├ out {out}\n')
                return Program(mem, des, inp, out, pos, rba, opc)
            nw_pos = pos + 2
            [pm1]  = mem[pos+1:nw_pos]
            value  = inp.pop(0)
            mem, store = store_value(mem, pm1, rba, md1, value)
            if dbg: print_instr(pos, [pm1], f'STO Input {value}.', f'Store {value} at {store}')

        elif opc == 4: 
            nw_pos = pos + 2
            [pm1]  = mem[pos+1:nw_pos]
            value  = get_value(mem, pm1, rba, md1)
            out.append(value)
            if dbg: print_instr(pos, [pm1], f'OUT Mem {value}.', f'Store {value} at output {len(out)-1}')

        elif opc == 5: 
            nw_pos = pos + 3
            [pm1, pm2] = mem[pos+1:nw_pos]
            value = get_value(mem, pm1, rba, md1)
            if value != 0: 
                nw_pos = get_value(mem, pm2, rba, md2)
            if dbg: 
                msg = f'Jump to {nw_pos}' if value != 0 else 'No jump'
                print_instr(pos, [pm1, pm2], f'JTR Compare {value} != 0.', msg)

        elif opc == 6: 
            nw_pos = pos + 3
            [pm1, pm2] = mem[pos+1:nw_pos]
            value = get_value(mem, pm1, rba, md1)
            if value == 0: 
                nw_pos = get_value(mem, pm2, rba, md2)
            if dbg: 
                msg = f'Jump to {nw_pos}' if value == 0 else 'No jump'
                print_instr(pos, [pm1, pm2], f'JFA Compare {value} == 0.', msg)

        elif opc == 7: 
            nw_pos = pos + 4
            [pm1, pm2, pm3] = mem[pos+1:nw_pos]
            value1 = get_value(mem, pm1, rba, md1)
            value2 = get_value(mem, pm2, rba, md2)
            result = int(value1 < value2)
            mem, store = store_value(mem, pm3, rba, md3, result)
            if dbg: print_instr(pos, [pm1, pm2, pm3], f'LES Compare {value1} < {value2}.', f'Store {result} at {store}')

        elif opc == 8:
            nw_pos = pos + 4
            [pm1, pm2, pm3] = mem[pos+1:nw_pos]
            value1 = get_value(mem, pm1, rba, md1)
            value2 = get_value(mem, pm2, rba, md2)
            result = int(value1 == value2)
            mem, store = store_value(mem, pm3, rba, md3, result)
            if dbg: print_instr(pos, [pm1, pm2, pm3], f'EQU Compare {value1} == {value2}.', f'Store {result} at {store}')

        elif opc == 9: 
            nw_pos = pos + 2
            [pm1]  = mem[pos+1:nw_pos]
            value  = get_value(mem, pm1, rba, md1)
            rba   += value
            if dbg: print_instr(pos, [pm1], f'ARB {rba} + {value}.', f'Set relative base to {rba}')

        elif opc == 99: 
            if dbg:
                print(f'{pos:5}: {opc:5}')
                print(f'├ out {out}\n')
            return Program(mem, des, inp, out, pos, rba, opc)

        else: raise Exception(f'Unknown opcode {opc} at pos {pos} with mem {mem[pos:pos+4]}')
        pos = nw_pos

if __name__ == "__main__":
    # Run tests
    assert create_run(
        des='Day 2',
        mem=[1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19, 1, 19, 9, 23, 1, 23, 6, 27, 2, 27, 13, 31, 1, 10, 31, 35, 1, 10, 35, 39, 2, 39, 6, 43, 1, 43, 5, 47, 2, 10, 47, 51, 1, 5, 51, 55, 1, 55, 13, 59, 1, 59, 9, 63, 2, 9, 63, 67, 1, 6, 67, 71, 1, 71, 13, 75, 1, 75, 10, 79, 1, 5, 79, 83, 1, 10, 83, 87, 1, 5, 87, 91, 1, 91, 9, 95, 2, 13, 95, 99, 1, 5, 99, 103, 2, 103, 9, 107, 1, 5, 107, 111, 2, 111, 9, 115, 1, 115, 6, 119, 2, 13, 119, 123, 1, 123, 5, 127, 1, 127, 9, 131, 1, 131, 10, 135, 1, 13, 135, 139, 2, 9, 139, 143, 1, 5, 143, 147, 1, 13, 147, 151, 1, 151, 2, 155, 1, 10, 155, 0, 4, 0, 99, 2, 14, 0, 0],
        ).out[0] == 4462686

    assert create_run(
        des='Day 5 part 1. 9 tests output 0. Last test outputs answer',
        mem=[3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226],
        inp=[1]
        ).out[9] == 7259358

    assert create_run(
        des='Day 5 part 2',
        mem=[3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226],
        inp=[5]
        ).out[0] == 11826654

    assert create_run(
        des='Day 7',
        mem=[3,8,1001,8,10,8,105,1,0,0,21,46,59,84,93,102,183,264,345,426,99999,3,9,1002,9,4,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,3,9,9,4,9,99,3,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1002,9,4,9,1001,9,4,9,102,2,9,9,1001,9,2,9,1002,9,3,9,4,9,99,3,9,1001,9,5,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99],
        inp=[0, 486]
        ).out[0] == 11697

    assert create_run(
        des='Day 9 part 1',
        mem=[1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,29,1011,1102,1,27,1009,1101,23,0,1008,1101,0,25,1017,1102,1,36,1016,1101,0,31,1018,1102,35,1,1012,1101,28,0,1004,1101,779,0,1024,1102,403,1,1026,1101,0,33,1010,1102,37,1,1015,1101,32,0,1014,1101,0,752,1023,1101,0,30,1013,1102,21,1,1001,1102,1,1,1021,1102,1,34,1002,1102,400,1,1027,1101,0,22,1007,1102,1,567,1028,1101,558,0,1029,1102,26,1,1006,1102,39,1,1005,1102,1,0,1020,1101,0,38,1000,1101,0,755,1022,1102,1,770,1025,1102,1,24,1003,1102,20,1,1019,109,28,21107,40,41,-9,1005,1019,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,-30,2107,38,7,63,1005,63,221,4,209,1105,1,225,1001,64,1,64,1002,64,2,64,109,-5,2102,1,8,63,1008,63,21,63,1005,63,251,4,231,1001,64,1,64,1106,0,251,1002,64,2,64,109,21,1207,-7,21,63,1005,63,267,1105,1,273,4,257,1001,64,1,64,1002,64,2,64,109,-1,1201,-7,0,63,1008,63,29,63,1005,63,293,1106,0,299,4,279,1001,64,1,64,1002,64,2,64,109,-4,1202,-3,1,63,1008,63,28,63,1005,63,319,1106,0,325,4,305,1001,64,1,64,1002,64,2,64,109,14,1206,-3,343,4,331,1001,64,1,64,1106,0,343,1002,64,2,64,109,-14,2108,21,-8,63,1005,63,361,4,349,1105,1,365,1001,64,1,64,1002,64,2,64,109,-9,1201,9,0,63,1008,63,27,63,1005,63,391,4,371,1001,64,1,64,1106,0,391,1002,64,2,64,109,27,2106,0,0,1106,0,409,4,397,1001,64,1,64,1002,64,2,64,109,-20,2101,0,0,63,1008,63,22,63,1005,63,431,4,415,1105,1,435,1001,64,1,64,1002,64,2,64,109,-7,1202,7,1,63,1008,63,22,63,1005,63,457,4,441,1105,1,461,1001,64,1,64,1002,64,2,64,109,8,1208,0,23,63,1005,63,479,4,467,1106,0,483,1001,64,1,64,1002,64,2,64,109,20,1205,-8,495,1105,1,501,4,489,1001,64,1,64,1002,64,2,64,109,-26,1208,4,28,63,1005,63,521,1001,64,1,64,1105,1,523,4,507,1002,64,2,64,109,15,21102,41,1,-2,1008,1015,41,63,1005,63,545,4,529,1106,0,549,1001,64,1,64,1002,64,2,64,109,18,2106,0,-7,4,555,1001,64,1,64,1106,0,567,1002,64,2,64,109,-30,1207,-3,35,63,1005,63,585,4,573,1105,1,589,1001,64,1,64,1002,64,2,64,109,14,1206,2,605,1001,64,1,64,1106,0,607,4,595,1002,64,2,64,109,-3,1205,5,621,4,613,1106,0,625,1001,64,1,64,1002,64,2,64,109,-5,21107,42,41,2,1005,1013,645,1001,64,1,64,1106,0,647,4,631,1002,64,2,64,109,-11,2108,42,5,63,1005,63,663,1106,0,669,4,653,1001,64,1,64,1002,64,2,64,109,4,21102,43,1,9,1008,1013,40,63,1005,63,693,1001,64,1,64,1106,0,695,4,675,1002,64,2,64,109,-1,2107,22,-2,63,1005,63,715,1001,64,1,64,1106,0,717,4,701,1002,64,2,64,109,7,21101,44,0,0,1008,1010,45,63,1005,63,741,1001,64,1,64,1106,0,743,4,723,1002,64,2,64,109,9,2105,1,4,1106,0,761,4,749,1001,64,1,64,1002,64,2,64,109,10,2105,1,-5,4,767,1001,64,1,64,1105,1,779,1002,64,2,64,109,-22,21108,45,43,10,1005,1017,799,1001,64,1,64,1105,1,801,4,785,1002,64,2,64,109,16,21101,46,0,-8,1008,1015,46,63,1005,63,827,4,807,1001,64,1,64,1105,1,827,1002,64,2,64,109,-7,2101,0,-7,63,1008,63,29,63,1005,63,851,1001,64,1,64,1106,0,853,4,833,1002,64,2,64,109,-5,2102,1,-3,63,1008,63,22,63,1005,63,877,1001,64,1,64,1106,0,879,4,859,1002,64,2,64,109,9,21108,47,47,-5,1005,1015,897,4,885,1105,1,901,1001,64,1,64,4,64,99,21102,27,1,1,21101,0,915,0,1105,1,922,21201,1,61784,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,942,0,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21102,1,957,0,1106,0,922,22201,1,-1,-2,1105,1,968,22101,0,-2,-2,109,-3,2105,1,0],
        inp=[1]
        ).out == [3241900951]

    assert create_run(des='Test: store and output 108', 
        mem=[3, 0, 4, 0, 99], inp=[108]).out[0] == 108

    assert create_run(des='Test: use parameters modes', 
        mem=[1002, 4, 3, 4, 33]).out == []

    assert create_run(des='Test: input == 8 (pos mode)', 
        mem=[3,9,8,9,10,9,4,9,99,-1,8], inp=[7]).out[0] == 0

    assert create_run(des='Test: input == 8 (imm mode)', 
        mem=[3,3,1108,-1,8,3,4,3,99], inp=[7]).out[0] == 0

    assert create_run(des='Test: input < 8 (pos mode)', 
        mem=[3,9,7,9,10,9,4,9,99,-1,8], inp=[7]).out[0] == 1

    assert create_run(des='Test: input < 8 (imm mode)', 
        mem=[3,3,1107,-1,8,3,4,3,99], inp=[7]).out[0] == 1

    assert create_run(des='Test: input != 0 (jumps, pos mode)', 
        mem=[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], inp=[7]).out[0] == 1

    assert create_run(des='Test: input != 0 (jumps, imm mode)', 
        mem=[3,3,1105,-1,9,1101,0,0,12,4,12,99,1], inp=[7]).out[0] == 1

    assert create_run(des='Test: input < 8: 999, 8: 1000, >8: 1001', 
        mem=[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
        inp=[8]).out[0] == 1000

    assert create_run(des='Test: halt program with exit opcode 3 when input buffer is empty', 
        mem=[3, 5, 3, 6, 99, -1, -1], inp=[1]).opc == 3

    assert create_run(des='Test: produce copy of self', 
        mem=[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]).out == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    assert create_run(des='Test: output 16-digit number', 
        mem=[1102,34915192,34915192,7,4,7,99,0]).out[0] == 1219070632396864