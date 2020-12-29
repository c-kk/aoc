with open('2020/day3/data.txt') as f:
    lines = f.read().split()

ypos = 0
xpos = 0
trees = 0

while True:
    ypos += 1
    xpos += 3
    if xpos >= 31: xpos -= 31

    try:
        character = lines[ypos][xpos]
        if character == "#":
            trees += 1
    except:
        break

print("Trees:", trees)
