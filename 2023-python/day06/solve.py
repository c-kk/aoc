import math

data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')

def count_ways_to_beat_the_record(race_time, distance_record):
    # Solve quadratic equation: ax**2 + bx + c = 0
    # button_time = race_time - travel_time
    # distance = button_time * travel_time
    # distance = (race_time - travel_time) * travel_time
    # distance = race_time * travel_time - travel_time * travel_time
    # - travel_time * travel_time + race_time * travel_time - distance = 0
    # travel_time * travel_time - race_time * travel_time + distance = 0
    a = 1
    b = - race_time
    c = distance_record

    # Calculate the discriminant
    d = (b**2) - (4*a*c)

    # Find the two boundary solutions
    travel_time1 = (- b - math.sqrt(d)) / (2 * a)
    travel_time2 = (- b + math.sqrt(d)) / (2 * a)

    # Adjust the boundary solutions if they are exactly integers
    # Because to beat the distance record, the distance traveled must be greater than the distance record  
    if travel_time1.is_integer(): travel_time1 += 1
    if travel_time2.is_integer(): travel_time2 -= 1

    # Count ways to beat the record
    print('The two boundary solutions for travel_time are {0} and {1}'.format(travel_time1, travel_time2))
    how_many_ways_to_beat_the_record = math.floor(travel_time2) + 1 - math.ceil(travel_time1)
    return how_many_ways_to_beat_the_record

# Part 1
print("*** Part 1 ***")
score_part1 = 0
race_times = [int(s) for s in lines[0].split(': ')[1].split()]
distances = [int(s) for s in lines[1].split(': ')[1].split()]
races = list(zip(race_times, distances))

for race_time, distance_record in races:
    print("Race time:", race_time, "Distance record:", distance_record)
    win_count = count_ways_to_beat_the_record(race_time, distance_record)
    print("Win count:", win_count)
    if win_count > 0: 
        score_part1 = score_part1 * win_count if score_part1 != 0 else win_count
print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
race_time = int(lines[0].split(': ')[1].replace(" ", ""))
distance_record = int(lines[1].split(': ')[1].replace(" ", ""))
score_part2 = count_ways_to_beat_the_record(race_time, distance_record)
print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)