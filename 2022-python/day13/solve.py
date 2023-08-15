# Used ChatGPT 4 while writing parts of the code

from functools import cmp_to_key

lines = open("data2.txt").read().split('\n')

def parse_string_to_nested_list(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '[':
            inner_list, consumed = parse_string_to_nested_list(s[i + 1:])
            result.append(inner_list)
            i += consumed + 1
        elif s[i] == ']':
            return result, i + 1
        elif s[i].isdigit():
            start = i
            while i < len(s) and s[i].isdigit():
                i += 1
            result.append(int(s[start:i]))
        else:
            i += 1
    return result[0]

def compare_pairs(pair1, pair2):
    if isinstance(pair1, int) and isinstance(pair2, int):
        return pair1 - pair2
    if isinstance(pair1, int): pair1 = [pair1]
    if isinstance(pair2, int): pair2 = [pair2]
    for left, right in zip(pair1, pair2):
        result = compare_pairs(left, right)
        if result != 0:
            return result
    return len(pair1) - len(pair2)

# Parsing the input data into nested lists
lists = [parse_string_to_nested_list(line) for line in lines if line]

# Part 1
score_part1 = sum(int((i + 2) / 2) for i in range(0, len(lists), 2) if compare_pairs(lists[i], lists[i + 1]) < 0)
print("Score part 1:", score_part1)

# Part 2
lists.extend([[[2]], [[6]]])
sorted_lines_corrected = sorted(lists, key=cmp_to_key(compare_pairs))
index_additional_line1 = sorted_lines_corrected.index([[2]]) + 1
index_additional_line2 = sorted_lines_corrected.index([[6]]) + 1
score_part2 = index_additional_line1 * index_additional_line2
print("Score part 2:", score_part2)