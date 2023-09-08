data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = [line.strip().split(": ") for line in open(filename).read().split('\n')]
jobs = {line[0]: line[1] for line in lines}

# Part 1
print("*** Part 1 ***")

def evaluate(monkey, jobs):
    # If the job is a number return it
    if jobs[monkey].isdigit():
        return int(jobs[monkey])
    
    # If the job is an operation do it
    operation = jobs[monkey].split()
    if len(operation) == 3:
        a, op, b = operation
        if op == '+':
            return evaluate(a, jobs) + evaluate(b, jobs)
        elif op == '-':
            return evaluate(a, jobs) - evaluate(b, jobs)
        elif op == '*':
            return evaluate(a, jobs) * evaluate(b, jobs)
        elif op == '/':
            return evaluate(a, jobs) // evaluate(b, jobs)
    return None

score_part1 = evaluate("root", jobs)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")

# Remove humn from the jobs to prevent its side from being solved
del jobs['humn']

# Figure out which side can be solved and which side contains humn
root_left, op, root_right = jobs['root'].split()
try: 
    root_solved = evaluate(root_left, jobs)
    pass
except KeyError: 
    root_not_solved = root_left
    root_solved = evaluate(root_right, jobs)
else: 
    root_not_solved = root_right

def find_humn_value_where_root_left_is_root_right_with_binary_search(lower_bound, upper_bound, direction, root_solved):
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2

        jobs['humn'] = str(mid)
        root_mid = evaluate(root_not_solved, jobs)
        mid_is_right = root_mid - root_solved == 0
        mid_is_too_high = direction * (root_mid - root_solved) > 0
        mid_is_right_or_too_high = mid_is_right or mid_is_too_high
        print(lower_bound, mid, upper_bound, root_mid, root_solved, mid_is_right_or_too_high)

        if mid_is_right_or_too_high:
            upper_bound = mid
        else: # mid is too low
            lower_bound = mid + 1
            
    return upper_bound if mid_is_right else -1

# Search for the right value for humn
# Start with a small range and increase it until humn is found
humn = -1 # -1 means humn has not been found yet
humn_lower_bound = 0 # Only positive integers
humn_upper_bound = 10 # Start with a small range
while humn == -1:
    jobs['humn'] = str(humn_lower_bound)
    root_at_lower_bound = evaluate(root_not_solved, jobs)
    jobs['humn'] = str(humn_upper_bound)
    root_at_upper_bound = evaluate(root_not_solved, jobs)
    direction = 1 if root_at_lower_bound < root_at_upper_bound else -1
    humn = find_humn_value_where_root_left_is_root_right_with_binary_search(humn_lower_bound, humn_upper_bound, direction, root_solved)
    humn_upper_bound *= 10 # Increase the range

score_part2 = humn
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)