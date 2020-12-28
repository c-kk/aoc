lines = open("2020/day10/data2.txt").read().split('\n')
numbers = list(map(int, lines))
numbers += [0, max(numbers) + 3]
numbers.sort()

def get_combinations(numbers):
    if len(numbers) == 1:
        return numbers[0]

    start_number = numbers[0]

    next_combinations = [numbers[1:][key:]
                    for key, number in enumerate(numbers[1:])
                    if number <= start_number + 3]

    recursed_combinations = [get_combinations(nc) for nc in next_combinations]
    # print(recursed_combinations)
    # exit()
    # flat_list = [c for combinations in recursed_combinations for c in combinations]

    # combinations = [next_number in next_numbers:

    return recursed_combinations

selection = numbers[0:4]
print(selection)

combinations = get_combinations(selection)
print(combinations)

pass
