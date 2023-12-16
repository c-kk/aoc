import math

data_version = input("Data version (1 or 2): ")

# Part 1
print("*** Part 1 ***")
filename = "data2.txt" if data_version == "2" else "data1a.txt"
lines = open(filename).read().split('\n')
instructions = [0 if char == 'L' else 1 for char in lines[0]]
nodes = {line[0:3]: [line[7:10], line[12:15]] for line in lines[2:]}
score_part1 = 0
current_node = 'AAA'
instruction_index = 0

while current_node != 'ZZZ':
    score_part1 += 1
    current_node = nodes[current_node][instructions[instruction_index % len(instructions)]]
    instruction_index += 1
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
filename = "data2.txt" if data_version == "2" else "data1b.txt"
lines = open(filename).read().split('\n')
instructions = [0 if char == 'L' else 1 for char in lines[0]]
nodes = {line[0:3]: [line[7:10], line[12:15]] for line in lines[2:]}
current_nodes = [node for node in nodes if node.endswith('A')]
instruction_index = 0
path_deltas = [0] * len(nodes)

while 0 in path_deltas:
    current_nodes = [nodes[node][instructions[instruction_index % len(instructions)]] for node in current_nodes]
    path_deltas = [instruction_index + 1 if node.endswith('Z') and delta == 0 else delta for node, delta in zip(current_nodes, path_deltas)]
    instruction_index += 1
score_part2 = math.lcm(*path_deltas)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)