lines = open("data.txt").read().split('\n')
width = len(lines[0])
height = len(lines)

# Part 1
print("*** Part 1 ***")
score_part1 = 0

# Visualize forest to see where the high trees are
for line in lines:
    for tree in line:
        tree = int(tree)
        if tree < 4:
            print('\033[97m' + str(tree) + '\033[0m', end="") # grey low tree
        elif tree < 7:
            print('\033[93m' + str(tree) + '\033[0m', end="") # yellow medium tree
        else: 
            print('\033[92m' + str(tree) + '\033[0m', end="") # green high tree
    print()

# Convert lines to array of rows
rows = [[0 for b in range(width)] for a in range(height)]
for y,line in enumerate(lines):
    for x,tree in enumerate(line):
        rows[y][x] = int(tree)

# Convert lines to array of columns
columns = [[0 for b in range(height)] for a in range(width)]
for y,line in enumerate(lines):
    for x,tree in enumerate(line):
        columns[x][y] = int(tree)

# Loop through rows and check for each tree if it's visible
for y,row in enumerate(rows):
    for x,tree in enumerate(row):
        column = columns[x]
        trees_left  = [-1] + row[:x]
        trees_right = [-1] + row[x+1:]
        trees_above = [-1] + column[:y]
        trees_below = [-1] + column[y+1:]
        #print(y,x,tree,'L', trees_left, 'R', trees_right, 'A', trees_above, 'B', trees_below)

        is_visible = tree > max(trees_left) or tree > max(trees_right) or tree > max(trees_above) or tree > max(trees_below)
        if is_visible:
            score_part1 += 1

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

# Loop through rows and calculate for each tree the scenic score
scenic_scores = [[0 for b in range(width)] for a in range(height)]
for y,row in enumerate(rows):
    for x,tree in enumerate(row):
        column = columns[x]

        trees_left = row[:x]
        see_left = 0
        for tree_left in trees_left[::-1]:
            see_left += 1
            if tree_left >= tree:
                break
        #print('Left', trees_left, tree, see_left)

        trees_right = row[x+1:]
        see_right = 0
        for tree_right in trees_right:
            see_right += 1
            if tree_right >= tree:
                break
        #print('Right', tree, trees_right, see_right)

        trees_above = column[:y]
        see_above = 0
        for tree_above in trees_above[::-1]:
            see_above += 1
            if tree_above >= tree:
                break
        #print('Above', trees_above, tree, see_above)

        trees_below = column[y+1:]
        see_below = 0
        for tree_below in trees_below:
            see_below += 1
            if tree_below >= tree:
                break
        #print('Below', tree, trees_below, see_below)

        scenic_score = see_left * see_right * see_above * see_below 
        scenic_scores[y][x] = scenic_score
        score_part2 = max(scenic_score, score_part2)

# Visualize forest to see the trees with a high scenic score
for scenic_scores_row in scenic_scores:
    for scenic_score in scenic_scores_row:
        display_score = int(9 * scenic_score/score_part2)
        if display_score == 0:
            print('\033[97m' + str(display_score) + '\033[0m', end="") # grey 0 score
        else: 
            print('\033[92m' + str(display_score) + '\033[0m', end="") # green >0 score
    print()

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
