import numpy as np

# https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-in-python

# Known grid dimensions
def breadth_first_search():
    pos    = (9, 1)
    wall   = "#"
    clear  = "."
    goal   = "*"
    width  = 10
    height = 5
    grid   = ["..........",
              "..*#...##.",
              "..##...#..",
              ".....###..",
              "......*..."]
    paths = [[pos]]
    seen = set([pos])
    while paths:
        path = paths.pop(0)
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width \
                and 0 <= y2 < height \
                and grid[y2][x2] != wall \
                and (x2, y2) not in seen: 
                paths.append(path + [(x2, y2)])
                seen.add((x2, y2))
                print('paths', paths)
                print('seen', seen)

# path = breadth_first_search()
# print('Shortest path', path)

secret_pos = (8,2)

# Unknown grid dimensions
def unknown_grid(move_cmd):
    grid = ["..........",
            "..*#...##.",
            "..##...#..",
            ".....###..",
            ".........."]

    moves  = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
    move   = moves[move_cmd]
    nw_pos = tuple(np.add(pos, move))
    
    try:
        x,y  = nw_pos
        char = grid[y][x]
    except:
        char = '#'

    if char != '#':
        secret_pos = nw_pos

    return char

def breadth_first_search_unknown():
    path  = [((0, 0), 0)]
    paths = [path]
    seen = set(path)
    while paths:
        path = paths.pop(0)
        pos, move_cmd = path[-1]

        print(pos, move_cmd)
        exit()
        # if path != (0, 0):
        #     diff = 
        
        moves = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
        for move_cmd, move in moves.items():
            # Calculate new position
            nw_pos = tuple(np.add(pos, move))
            
            # Continue if already seen position
            if nw_pos in seen:
                continue

            # Send move to droid and receive character
            char = unknown_grid(move_cmd)

            # Continue when a wall is hit
            if char == '#':
                continue

            # Finish when goal is reached
            if char == '*':
                return path + [nw_pos]

            # Reverse step when a path is reached
            if char == '.':
                _ = unknown_grid((move_cmd - 2) % 4)
                paths.append(path + [nw_pos], move_cmd)
                seen.add(nw_pos)            

            # print(char)

path = breadth_first_search_unknown()
print('Shortest path', path)