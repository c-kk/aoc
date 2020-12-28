import math

with open('data.txt') as f:
    lines = f.read().split()

slopes = [
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [1, 2],
]

trees_per_slope = []

for slope in slopes:
    ypos = 0
    xpos = 0
    trees = 0

    while True:
        ypos += slope[1]
        xpos += slope[0]
        if xpos >= 31: xpos -= 31

        try:
            character = lines[ypos][xpos]
            if character == "#":
                trees += 1
        except:
            break

    trees_per_slope.append(trees)
    print("Slope:", slope, "Trees:", trees)

multiplied = math.prod(trees_per_slope)
print("Multiplied:", multiplied)
