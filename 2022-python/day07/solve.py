lines = open("data.txt").read().split('\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

found_dirs = []
dir_index = 0
directories = {'/': []}
current_directory = '/'

for index, line in enumerate(lines):
    print(index, line)

    if line.startswith('$ ls') or line.startswith('$ cd ..'):
        continue

    if line.startswith('dir'):
        found_directory = line[4:] + "-" + str(dir_index)
        found_dirs.append(found_directory)
        dir_index += 1

        print('Found directory:', found_directory)
        directories[found_directory] = []
        directories[current_directory].append(found_directory)
        print('Directories:', directories)

    elif line.startswith('$ cd '):
        directory = line[5:]
        for found_dir_index, found_dir in enumerate(found_dirs):
            if found_dir.startswith(directory + '-'):
                current_directory = found_dir
                del found_dirs[found_dir_index]
                break

        print('Current directory:', current_directory)

    else:
        found_filesize = int(line.split(" ")[0])
        print('Found filesize:', found_filesize)
        directories[current_directory].append(found_filesize)
        print('Directories:', directories)

def calculate_directory_size(directory):
    dictory_size = 0
    directory_contents = directories[directory]
    print("Directory:", directory, "contents", directory_contents)

    for filesize_or_dir in directory_contents:
        is_filesize = isinstance(filesize_or_dir, int)
        if is_filesize:
            dictory_size += filesize_or_dir
        else:
            found_directory = filesize_or_dir
            dictory_size += calculate_directory_size(found_directory)

    print("Directory:", directory, "size", dictory_size)
    return dictory_size

directory_sizes = {}
for directory in directories.keys():
    dictory_size = calculate_directory_size(directory)
    directory_sizes[directory] = dictory_size
    print('Directory sizes:', directory_sizes)

    if dictory_size <= 100000:
        score_part1 += dictory_size

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

space_needed = directory_sizes['/'] - 40000000
print("Space needed", space_needed)

directory_sizes_sorted = dict(sorted(directory_sizes.items(), key=lambda x:x[1]))
for directory, size in directory_sizes_sorted.items():
    if size > space_needed:
        print("Directory", directory, "found with size", size)
        score_part2 = size
        break

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)
