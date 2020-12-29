import itertools

lines = open("2020/day9/data.txt").read().split('\n')
numbers = [int(line) for line in lines]

pointer = 0
joy = 25

while True:
    preamble = numbers[pointer:pointer+joy]
    target = numbers[pointer+joy]
    combos = list(itertools.combinations(preamble, 2))
    found = False
    for combo in combos:
        summed = combo[0] + combo[1]
        if summed == target and not found:
            # print(combo[0], combo[1], target)
            found = True
    if not found:
        print("Target", target)
        break
    pointer += 1

def find_contirange(pointer, numbers, target):
    contirange = []
    while True:
        contirange.append(numbers[pointer])
        summed = sum(contirange)
        if summed == target:
            return True, contirange
        if summed > target:
            return False, contirange
        pointer += 1

pointer = 0
while True:
    found, contirange = find_contirange(pointer, numbers, target)
    if found:
        print("Contirange", contirange, "min", min(contirange), "max", max(contirange))
        print("Weakness", min(contirange) + max(contirange))

        break
    pointer += 1

pass
