data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
blocks = open(filename).read().split('\n\n')

# Part 1
print("*** Part 1 ***")
score_part1 = 0

seeds = list(map(int, blocks[0].split(': ')[1].split()))
maps = [[[int(number) for number in line.split(' ')] for line in block.split('\n')[1:]] for block in blocks[1:]]

for seed in seeds:
    print("Seed:", seed)
    for map in maps:
        for dest_start, src_start, length in map:
            if seed >= src_start and seed < src_start + length:
                seed = dest_start + (seed - src_start)
                break
        print(map, seed)
    score_part1 = min(seed, score_part1) if score_part1 != 0 else seed

print("Score part 1:", score_part1)

# Part 2
# Reverse search
# Start at location 1 and work backwards to find the first location that has a seed
print("*** Part 2 ***")
score_part2 = 0
seed_pairs = list(zip(seeds[::2], seeds[1::2]))
location = 0
seed_present = False
maps_reversed = maps[::-1]

while True:
    location += 1
    print("Location:", location)

    seed = location
    for map in maps_reversed:
        for src_start, dest_start, length in map:
            if seed >= src_start and seed < src_start + length:
                seed = dest_start + (seed - src_start)
                break
        # print(map, seed)
    
    for seed_start, seed_range in seed_pairs:
        seed_present = seed_present or (seed >= seed_start and seed <= seed_start + seed_range - 1)
    if seed_present: 
        break

score_part2 = location

print("Score part 2:", score_part2)
# 11611182 is correct

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)