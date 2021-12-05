import collections
import math
import re
import sys

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')

def domask(arg, mask):
    arg |= int(mask.replace('X', '0'), 2)
    arg &= int(mask.replace('X', '1'), 2)
    return arg


def allmasks(mask):
    if not mask:
        yield ''
        return
    for m in allmasks(mask[1:]):
        if mask[0] == '0':
            yield 'X' + m  # leave unchanged
        elif mask[0] == '1':
            yield '1' + m  # replace with 1
        elif mask[0] == 'X':
            yield '0' + m  # replace with 0
            yield '1' + m  # replace with 1


mask = None
mem = collections.defaultdict(int)
for line in lines:
    op, arg = line.split(' = ')
    if op == 'mask':
        mask = arg
    else:
        pos = int(op[4:-1])
        # part 1:
        # mem[pos] = domask(int(arg), mask)
        for m in allmasks(mask):
            mem[domask(pos, m)] = int(arg)

print(sum(mem.values()))