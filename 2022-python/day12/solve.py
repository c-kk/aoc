from pathfinding import *

lines = open("data2.txt").read().split('\n')
for line in lines:
    print(line)

# Part 1
print("*** Part 1 ***")

class GridWithHeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.heights: dict[GridLocation, int] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return 1
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        neighbors_in_bounds = [neighbor for neighbor in neighbors if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height]
        passable_neighbors = [neighbor for neighbor in neighbors_in_bounds if (self.heights[id] + 1) >= self.heights[neighbor]]
        return passable_neighbors

width = len(lines[0])
height = len(lines)
heightmap = GridWithHeights(width, height)

for y,line in enumerate(lines):
    for x,height_char in enumerate(line):
        if height_char == 'S':
            height = 0
            start = (x,y)
        elif height_char == 'E':
            height = 25
            goal = (x,y)
        else:
            height = ord(height_char) - 97
        heightmap.heights[(x, y)] = height 

came_from = breadth_first_search(heightmap, start, goal)
path=reconstruct_path(came_from, start=start, goal=goal)
draw_grid(heightmap, path=path)
score_part1 = len(path) - 1
print("Score part 1:", score_part1)   

# Part 2
print("*** Part 2 ***")
starting_locations: list[GridLocation] = [loc for loc, height in heightmap.heights.items() if height == 0]
best_path = path
score_part2 = score_part1

for start in starting_locations:
    came_from = breadth_first_search(heightmap, start, goal)
    #came_from, cost_so_far = dijkstra_search(heightmap, start, goal) # Dijkstra search isn't quicker for this puzzle
    #came_from, cost_so_far = a_star_search(heightmap, start, goal) # A* search isn't quicker for this puzzle
    path=reconstruct_path(came_from, start=start, goal=goal)
    path_length = len(path) - 1
    if path_length > 0 and path_length < score_part2:
        best_path = path
        score_part2 = path_length

draw_grid(heightmap, path=best_path)
print("Score part 2:", score_part2)   