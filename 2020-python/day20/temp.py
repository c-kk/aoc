def explore(image, monster, x, y):
    for delta_y, row in enumerate(monster):
        for delta_x, monster_char in enumerate(row):
            try:
                image_char = image[y + delta_y][x + delta_x]
                if monster_char == 1 and image_char != 1:
                    return False
            except:
                return False
    return True

def find_monster_in_image(image, monster):
    for y, row in enumerate(image):
        for x, char in enumerate(row):
            print(x, y, char)
            if explore(image, monster, x, y):
                print(f"Found monster at {x}, {y}")
                return x, y
    print(f"Monster not found")
    return None, None


image = [
    [9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9],
    [1, 1, 9, 9, 1, 9, 9],
    [1, 9, 1, 1, 9, 9, 9]
]

monster = [
    [9, 1, 9, 9, 1],
    [1, 9, 1, 1, 9],
]

find_monster_in_image(image, monster)