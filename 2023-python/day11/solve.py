data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
rows = [[char for char in line] for line in lines]

# Print galaxy
def print_galaxy(rows):
    for row in rows:
        for char in row:
            print(char, end='')
        print()
print_galaxy(rows)

# Find empty rows and columns 
empty_row_indexes = [row_index for row_index, row in enumerate(rows) if row.count('.') == len(row)]
columns = [[row[col_index] for row in rows] for col_index in range(len(rows[0]))]
empty_column_indexes = [col_index for col_index, col in enumerate(columns) if col.count('.') == len(col)]

# Expand the galaxy
# Make row and column index lists for expension
# Increase index space of empty rows and columns in expanded index lists
def expand_indexes(rows, empty_row_indexes, empty_column_indexes, expand_by):
    expanded_row_indexes = list(range(len(rows)))
    expanded_col_indexes = list(range(len(rows[0])))

    for empty_row_index in empty_row_indexes:
        for row_index in range(empty_row_index + 1, len(rows[0])):
            expanded_row_indexes[row_index] += expand_by

    for empty_col_index in empty_column_indexes:
        for col_index in range(empty_col_index + 1, len(rows)):
            expanded_col_indexes[col_index] += expand_by

    return expanded_row_indexes, expanded_col_indexes

def find_galaxies(rows, expanded_row_indexes, expanded_col_indexes):
    galaxies = []
    for row_index, row in enumerate(rows):
        for col_index, char in enumerate(row):
            if char == '#':
                expended_row_index = expanded_row_indexes[row_index]
                expended_col_index = expanded_col_indexes[col_index]
                galaxies.append((expended_row_index, expended_col_index))
    return galaxies

def make_unique_pairs(galaxies):
    galaxy_pairs = set()
    for galaxy1 in galaxies:
        for galaxy2 in galaxies:
            if galaxy1 != galaxy2 and (galaxy2, galaxy1) not in galaxy_pairs:
                galaxy_pairs.add((galaxy1, galaxy2))
    return galaxy_pairs

def calculate_distances(galaxy_pairs):
    galaxy_pair_distances = {}
    for galaxy_pair in galaxy_pairs:
        galaxy1, galaxy2 = galaxy_pair
        galaxy1_row, galaxy1_col = galaxy1
        galaxy2_row, galaxy2_col = galaxy2
        distance = abs(galaxy1_row - galaxy2_row) + abs(galaxy1_col - galaxy2_col)
        galaxy_pair_distances[galaxy_pair] = distance
    return galaxy_pair_distances

def sum_distances(galaxy_pair_distances):
    total_distance = 0
    for galaxy_pair_distance in galaxy_pair_distances.values():
        total_distance += galaxy_pair_distance
    return total_distance

# Part 1
print("*** Part 1 ***")
expanded_row_indexes, expanded_col_indexes = expand_indexes(rows, empty_row_indexes, empty_column_indexes, 1)
galaxies = find_galaxies(rows, expanded_row_indexes, expanded_col_indexes)
galaxy_pairs = make_unique_pairs(galaxies)
galaxy_pair_distances = calculate_distances(galaxy_pairs)
score_part1 = sum_distances(galaxy_pair_distances)
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
expanded_row_indexes, expanded_col_indexes = expand_indexes(rows, empty_row_indexes, empty_column_indexes, 999999)
galaxies = find_galaxies(rows, expanded_row_indexes, expanded_col_indexes)
galaxy_pairs = make_unique_pairs(galaxies)
galaxy_pair_distances = calculate_distances(galaxy_pairs)
score_part2 = sum_distances(galaxy_pair_distances)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)