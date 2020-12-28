import time
import copy

lines = open("2020/day10/data.txt").read().split('\n')
numbers = list(map(int, lines))
numbers.append(0)
numbers.append(max(numbers) + 3)
numbers.sort()

def get_combos(combos, solutions, cache, iteration):
    is_finished = True
    new_combos = []

    for combo in combos:
        time.sleep(0.01)

        [todo_list, done_list] = combo
        # print(todo_list, done_list)

        last_number = done_list[0]
        if last_number == 0:
            solutions.add(tuple(done_list))
            continue

        is_finished = False

        # if str(todo_list) in cache:
        #     for new_combo in cache[combo]:
        #         new_combos.append(new_combo)
        #     continue

        iteration += 1
        # print(iteration)
        # print(iteration, todo_list, done_list)

        previous_numbers = todo_list[-3:]

        for previous_number in previous_numbers:
            is_an_option = (last_number - previous_number) <= 3
            if is_an_option:
                new_todo_list = copy.deepcopy(todo_list)
                new_done_list = copy.deepcopy(done_list)
                index_of_previous_number = new_todo_list.index(previous_number)
                del new_todo_list[index_of_previous_number:]
                new_done_list.insert(0, previous_number)
                # solution_cache.append([new_todo_list, new_done_list])
                new_combo = [new_todo_list, new_done_list]
                new_combos.append(new_combo)

        # cache[str(todo_list)] = new_combos
    return is_finished, new_combos, solutions, cache, iteration

last_number = numbers.pop()
combos = [[numbers, [last_number]]]

cache = dict()
solutions = set()
iteration = 0
is_finished = False
while not is_finished:
    is_finished, combos, solutions, cache, iteration = get_combos(combos, solutions, cache, iteration)

# print(solutions)
print(cache)
# print(*cache, sep='\n')

answer2 = len(solutions)
print(iteration, answer2)

pass
