data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
ori_index_and_numbers = [(index, int(line)) for index, line in enumerate(open(filename).read().split('\n'))]
mov_index_and_numbers = ori_index_and_numbers.copy()

def move_item_in_list(lst, item_to_move, steps):
    index = lst.index(item_to_move)
    item = lst.pop(index)
    new_index = (index + steps) % len(lst)
    lst.insert(new_index, item)
    return lst

# Part 1
print("*** Part 1 ***")
# Move items
for index_and_number in ori_index_and_numbers:
    index, number = index_and_number
    mov_index_and_numbers = move_item_in_list(mov_index_and_numbers, index_and_number, number)

# Get the 1000th, 2000th and 3000th number after 0
mov_numbers = [number for _, number in mov_index_and_numbers]
zero_index = mov_numbers.index(0)
numbers_after_zero = [(mov_numbers[(zero_index + nth) % len(mov_numbers)]) for nth in [1000, 2000, 3000]]
score_part1 = sum(numbers_after_zero)

print(numbers_after_zero)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

# Apply key
key = 811589153
ori_index_and_numbers2 = [(index, key * number) for index, number in ori_index_and_numbers]
mov_index_and_numbers2 = ori_index_and_numbers2.copy()

# Move items ten times
for _ in range(10):
    for index_and_number in ori_index_and_numbers2:
        index, number = index_and_number
        mov_index_and_numbers2 = move_item_in_list(mov_index_and_numbers2, index_and_number, number)

# Get the 1000th, 2000th and 3000th number after 0
mov_numbers2 = [number for _, number in mov_index_and_numbers2]
zero_index = mov_numbers2.index(0)
numbers_after_zero2 = [(mov_numbers2[(zero_index + nth) % len(mov_numbers2)]) for nth in [1000, 2000, 3000]]
score_part2 = sum(numbers_after_zero2)

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)