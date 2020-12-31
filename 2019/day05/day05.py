import attr

@attr.s
class Mind():
    mem = attr.ib()
    pos = attr.ib()
    inp = attr.ib()
    opc = attr.ib(default=None)
    pam = attr.ib(default=None)

    def get_mem(self, address):
        return self.mem[address]

    def set_mem(self, address, value):
        self.mem[address] = value

    def get_opcode(self):
        pos = self.pos
        value = self.mem[pos]
        opcode = abs(value) % 100
        parameter_modes = [value // 100 % 10, value // 1000 % 10, value // 10000 % 10]

        msg = f'{pos:3}: opcode {opcode:2} pam {parameter_modes} '
        self.pos += 1
        self.opc = opcode
        self.pam = parameter_modes
        return opcode, msg

    def get_value_or_parameter(self):
        parameter, msg = self.get_parameter()

        mode = self.pam.pop(0)
        if mode == 0:
            value = self.mem[parameter]
            msg  += f'(mode {mode}, value {value})'
        return value, msg

    def get_parameter(self):
        parameter = self.mem[self.pos]
        self.pos += 1
        msg = f'par {parameter}'
        return parameter, msg

    # def get_parameters(self, amount):
    #     parameters = self.mem[self.pos:self.pos+amount]
    #     msg = 'par [' + ', '.join([f'{par:3}' for par in parameters]) + '] '
    #     self.pos += amount
    #     return parameters, msg

    def get_input(self, amount):
        inp = self.inp.pop(0)
        msg = 'inp {inp}' 
        return inp, msg

def add_1(mind: Mind):
    # [par1, par2, par3], msg = mind.get_parameters(3)
    value1 = mind.get_value_or_parameter()
    value2 = mind.get_value_or_parameter()
    result = value1 + value2
    store  = mind.get_parameter()
    mind.set_mem(store, result)
    msg += f'Add {value1:7} + {value2:7}. Store at {store:3}'
    return mind, msg
    
def multiply_2(mind: Mind):
    value1 = mind.get_value_or_parameter()
    value2 = mind.get_value_or_parameter()
    result = value1 * value2
    store  = mind.get_parameter()
    mind.set_mem(store, result)
    msg += f'Mul {value1:7} * {value2:7}. Store at {store:3}'
    return mind, msg

def store_3(mind: Mind):
    [par1], par_msg = mind.get_parameters(1)
    [inp1], inp_msg = mind.get_inputs(1)
    mind.set_mem(par1, inp1)
    msg = par_msg + inp_msg + f'Store {inp1:7} at {par1:3}'
    return mind, msg

def output_4(mind: Mind):
    [par1], msg = mind.get_parameters(1)
    value1 = mind.get_mem(par1)
    msg += f'Output {value1:7} from {par1:3}'
    return mind, msg

def exit_99(mind: Mind):
    # msg  = msg_start(mem, pos) + f'Exit, returning mem[0]={mem[0]}'
    msg = 'Exit'
    return mind, msg

opcode_lookup = {
    1: add_1, 
    2: multiply_2,
    3: store_3,
    4: output_4,
    99: exit_99
}

def run_program(mem, inputs, debug=False):
    mind = Mind(mem.copy(), pos=0, inp=inputs)
    # sprint(mind.mem)

    while True:
        opcode, opcode_msg = mind.get_opcode()
        func = opcode_lookup[opcode]
        mind, func_msg = func(mind)
            
        msg = opcode_msg + func_msg
        if debug: print(msg)
        if opcode == 99: 
            # print(mind.mem)
            return mind.get_mem(0)

def run_day_2():
    mem = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19, 1, 19, 9, 23, 1, 23, 6, 27, 2, 27, 13, 31, 1, 10, 31, 35, 1, 10, 35, 39, 2, 39, 6, 43, 1, 43, 5, 47, 2, 10, 47, 51, 1, 5, 51, 55, 1, 55, 13, 59, 1, 59, 9, 63, 2, 9, 63, 67, 1, 6, 67, 71, 1, 71, 13, 75, 1, 75, 10, 79, 1, 5, 79, 83, 1, 10, 83, 87, 1, 5, 87, 91, 1, 91, 9, 95, 2, 13, 95, 99, 1, 5, 99, 103, 2, 103, 9, 107, 1, 5, 107, 111, 2, 111, 9, 115, 1, 115, 6, 119, 2, 13, 119, 123, 1, 123, 5, 127, 1, 127, 9, 131, 1, 131, 10, 135, 1, 13, 135, 139, 2, 9, 139, 143, 1, 5, 143, 147, 1, 13, 147, 151, 1, 151, 2, 155, 1, 10, 155, 0, 99, 2, 14, 0, 0]
    inp = []
    result = run_program(mem, inp, False)
    assert result == 4462686
    print('Day 2:', result)

def test_print_input():
    mem = [3, 0, 4, 0, 99]
    inp = [108]
    result = run_program(mem, inp, False)
    assert result == 108
    print('Print input:', result)

def run_day_5():
    mem = [3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
    inp = [1]
    result = run_program(mem, inp, True)
    assert result == 4462686
    print('Day 2:', result)

run_day_2()
test_print_input()
run_day_5()