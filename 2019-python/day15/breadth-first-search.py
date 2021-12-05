# https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-in-python
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

path = breadth_first_search()
print('Shortest path', path)