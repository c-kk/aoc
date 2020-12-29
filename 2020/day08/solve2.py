import attr
import copy

lines = open("2020/day8/data.txt").read().split('\n')

@attr.s
class Group:
    instr = attr.ib()
    val = attr.ib(converter=int)

    def run(self, index, accumulator):
        if self.instr == 'nop':
            index += 1
        elif self.instr == 'acc':
            accumulator += self.val
            index += 1
        elif self.instr == 'jmp':
            index += self.val
        return index, accumulator

groups = []
for line in lines:
    split = line.split(" ")
    group = Group(*split)
    groups.append(group)

def run(_groups):
    # print(_groups)
    _idx = 0
    _accumulator = 0
    _runned_instructions = []

    while _idx < len(_groups):
        _group: Group = _groups[_idx]

        if _idx in _runned_instructions:
            break
        _runned_instructions.append(_idx)

    return group.run(_idx, _accumulator)

accumulator = 0
change_index = 0

while True:
    new_groups = copy.deepcopy(groups)
    if change_index >= len(new_groups):
        break
    group: Group = new_groups[change_index]

    if group.instr == 'nop':
        print(change_index, "changed to jmp")
        group.instr = 'jmp'
    elif group.instr == 'jmp':
        print(change_index, "changed to nop")
        group.instr = 'nop'
        # print(new_groups)
    new_groups[change_index] = group

    idx, accumulator = run(new_groups)
    last_idx = len(new_groups) - 1
    if last_idx <= idx:
        print('found', last_idx, idx, accumulator, change_index)
        break
    else:
        print('not found', last_idx, idx, accumulator, change_index)
    change_index += 1

print(accumulator)
pass