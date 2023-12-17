data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
histories = [[int(number) for number in line.split(' ')] for line in lines]

# Part 1
print("*** Part 1 ***")
score_part1 = 0
for history in histories:
    diffs = [history.copy()]
    while diffs[0].count(0) != len(diffs[0]):
        diffs.insert(0, [diffs[0][i] - diffs[0][i - 1] for i in range(1, len(diffs[0]))])

    for diff_index, diff in enumerate(diffs):
        if diff_index == 0:
            diff.append(0)
        else:
            diff.append(diff[-1] + diffs[diff_index - 1][-1])    
    print('Diffs:', diffs)

    prediction = diffs[-1][-1]
    score_part1 += prediction
    print('Prediction:', prediction)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0
for history in histories:
    diffs = [history.copy()]
    while diffs[0].count(0) != len(diffs[0]):
        diffs.insert(0, [diffs[0][i] - diffs[0][i - 1] for i in range(1, len(diffs[0]))])

    for diff_index, diff in enumerate(diffs):
        if diff_index == 0:
            diff.insert(0, 0)
        else:
            diff.insert(0, diff[0] - diffs[diff_index - 1][0])    
    print('Diffs:', diffs)

    prediction = diffs[-1][0]
    score_part2 += prediction
    print('Prediction:', prediction)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)