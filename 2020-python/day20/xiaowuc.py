def rotgrid(g):
  ng = []
  n = len(g)
  for i in range(n):
    ng.append(['#'] * n)
  for i in range(n):
    for j in range(n):
      ng[j][n-1-i] = g[i][j]
  return ng

def flipgrid(g):
  ng = []
  n = len(g)
  for i in range(n):
    ng.append(g[i][::-1])
  return ng

def getforcedrotations(g):
  ret = []
  ret.append(g)
  ret.append(rotgrid(ret[-1]))
  ret.append(rotgrid(ret[-1]))
  ret.append(rotgrid(ret[-1]))
  ret.append(flipgrid(g))
  ret.append(rotgrid(ret[-1]))
  ret.append(rotgrid(ret[-1]))
  ret.append(rotgrid(ret[-1]))
  return ret

def force(g):
  pattern = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".split("\n")
  pattern = [x for x in pattern if x]
  for realgrid in getforcedrotations(g):
    used = []
    for row in realgrid:
      used.append([False] * len(row))
    i = 0
    while i + len(pattern) <= len(realgrid):
      j = 0
      while j + len(pattern[0]) <= len(realgrid[i]):
        good = True
        for a in range(len(pattern)):
          for b in range(len(pattern[a])):
            if pattern[a][b] == '#' and realgrid[i+a][j+b] != '#':
              good = False
        if good:
          for a in range(len(pattern)):
            for b in range(len(pattern[a])):
              if pattern[a][b] == '#':
                used[i+a][j+b] = True
        j += 1
      i += 1
    ret = 0
    for i in range(len(realgrid)):
      for j in range(len(realgrid[i])):
        if realgrid[i][j] == '#' and not used[i][j]:
          ret += 1
    print(ret)

def part2(g):
  n = len(g)
  realgrid = []
  for i in range(n):
    for j in range(n):
      smallgrid = []
      for k in range(10):
        if k in [0, 9]:
          continue
        cand = []
        for a in range(10):
          if k in [0, 9] or a in [0, 9]:
            continue
          if g[i][j][1] & (2 ** (99 - (10 * k + a))):
            cand.append('#')
          else:
            cand.append('.')
        smallgrid.append(cand)
      srow = len(smallgrid) * i
      for rowi, row in enumerate(smallgrid):
        while srow + rowi >= len(realgrid):
          realgrid.append([])
        realgrid[srow+rowi].extend(row)
  force(realgrid)

def rot(mask):
  val = 0
  for i in range(10):
    for j in range(10):
      idx = 10 * j + 9 - i
      if mask & (2**(10*i+j)):
        val |= 2 ** idx
  return val

def flip(mask):
  val = 0
  for i in range(10):
    for j in range(10):
      idx = 10 * i + 9 - j
      if mask & (2**(10*i+j)):
        val |= 2 ** idx
  return val

def get_all_rotations(mask):
  ret = []
  ret.append(mask)
  ret.append(rot(ret[-1]))
  ret.append(rot(ret[-1]))
  ret.append(rot(ret[-1]))
  ret.append(flip(mask))
  ret.append(rot(ret[-1]))
  ret.append(rot(ret[-1]))
  ret.append(rot(ret[-1]))
  return ret

def get_top(mask):
  idx = 99
  val = 0
  for i in range(10):
    val *= 2
    if mask & (2**idx):
      val += 1
    idx -= 1
  return val

def get_bottom(mask):
  return mask & 1023

def get_left(mask):
  val = 0
  idx = 99
  for i in range(10):
    val *= 2
    if mask & (2 ** idx):
      val += 1
    idx -= 10
  return val

def get_right(mask):
  val = 0
  idx = 90
  for i in range(10):
    val *= 2
    if mask & (2 ** idx):
      val += 1
    idx -= 10
  return val

# Starts with: grid, 0, 0, tiles, used
def dfs(grid, row, column, tiles, used):
  # Print grid nicely
  for line in grid: 
    for value in line:
      if value == -1: 
        print(value, end=' ')
      else:
        print(value[0], end=' ')
    print('')
  print(f"{row=}, {column=}, {used=}\n")

  # When the last row is finished, calculate the answers
  if row == len(grid):
    print("Part 1:", grid[0][0][0] * grid[0][-1][0] * grid[-1][0][0] * grid[-1][-1][0])
    part2(grid)
    exit(0)
    return

  # When the column is finished go to the next row
  if column == len(grid[row]):
    dfs(grid, row + 1, 0, tiles, used)
    return

  for tile_id, value in tiles:
    if tile_id in used:
      continue

    # In some magic way the tile value is rotated and flipped to get all 8 rotations
    all_rotations = get_all_rotations(value)
    # print(all_rotations)

    for cand in all_rotations:
      good = True
      if row > 0:
        value_of_cell_above = grid[row - 1][column][1]
        good &= get_top(cand) == get_bottom(value_of_cell_above)

      if column > 0:
        value_of_cell_to_the_left = grid[row][column - 1][1]
        good &= get_left(cand) == get_right(value_of_cell_to_the_left)

      if good:
        grid[row][column] = (tile_id, cand)
        used.add(tile_id)
        dfs(grid, row, column + 1, tiles, used)
        
        # Recursion is unsuccesful when reaching this point => undo last tile 
        used.discard(tile_id)
        assert tile_id not in used
        grid[row][column] = -1

# Tiles are tuples (id of tile, value => binary of tile converted to decimal value)
tiles = []
while True:
  try:
    string = input()
    assert string.startswith("Tile")
    string = string[5:-1]
    id = int(string)
    dec_value = 0
    for i in range(10):
      string = input()
      for j in range(10):
        dec_value *= 2
        if string[j] == '#':
          dec_value += 1
    tiles.append((id, dec_value))
    input()
  except EOFError:
    break
print(tiles)
print('')

# Calculate grid width
size = 1
while size * size < len(tiles):
  size += 1
assert size*size == len(tiles), f"{size} {len(tiles)}"

# Create grid, all cells have value of -1
grid = []
for i in range(size):
  grid.append([-1] * size)

# Create a set for used tiles, so you don't have to double check them
used = set()

# Start the recursion
dfs(grid, 0, 0, tiles, used)