import itertools

lines = open("2020/day9/data.txt").read().split('\n')
numbers = list(map(int, lines))
pointer = 0
pre = 25

while True:
    preamble = numbers[pointer:pointer + pre]
    target = numbers[pointer + pre]
    combos = itertools.combinations(preamble, 2)
    found = target in map(sum, combos)
    if not found:
        print("Part1", target)
        break
    pointer += 1

def find_conti_range(pointer, numbers, target):
    end = pointer + 1
    conti_range = []
    while sum(conti_range) < target:
        conti_range = numbers[pointer:end]
        end += 1
    if sum(conti_range) == target:
        return True, conti_range
    return False, conti_range

pointer = 0
while True:
    found, conti_range = find_conti_range(pointer, numbers, target)
    if found:
        break
    pointer += 1

print("Part2", min(conti_range) + max(conti_range))
pass
