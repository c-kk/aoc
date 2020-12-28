import attr

@attr.s(frozen=True)
class Instruction:
    op = attr.ib()
    arg = attr.ib(converter=int)

    @classmethod
    def from_string(cls, string):
        op, arg = string.split(" ")
        return cls(op, arg)

    def run(self, pointer, accumulator):
        print(pointer, accumulator, ':', self.op, self.arg)

        delta_poi = {'nop': 1, 'acc': 1, 'jmp': self.arg}
        delta_acc = {'nop': 0, 'acc': self.arg, 'jmp': 0}

        pointer += delta_poi[self.op]
        accumulator += delta_acc[self.op]

        return pointer, accumulator

@attr.s(frozen=True)
class Program:
    instructions = attr.ib()

    @classmethod
    def from_lines(cls, lines):
        instructions = [Instruction.from_string(line) for line in lines]
        return cls(instructions)

    def run(self):
        pointer = 0
        accumulator = 0
        runned_instructions = []

        while True:
            instruction_exists = 0 <= pointer < len(self.instructions)
            if not instruction_exists:
                return "Finished at", pointer, accumulator

            in_loop = pointer in runned_instructions
            if in_loop:
                return "Looping at", pointer, accumulator
            else:
                runned_instructions.append(pointer)

            pointer, accumulator = self.instructions[pointer].run(pointer, accumulator)


lines = open("2020/day8/data.txt").read().split('\n')
program = Program.from_lines(lines)
message, pointer, accumulator = program.run()
print(message, pointer, accumulator)
pass
