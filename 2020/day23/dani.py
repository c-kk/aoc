input = "389125467" # test input
#input = "463528179" # own input

import time
from tqdm import tqdm

def step(cups, current_cup_index):
    ## The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
    current_cup_label = cups[current_cup_index]
    removed_cups = [cups[(current_cup_index+i+1) % nr_cups] for i in range(3)]
    cups = [cup for cup in cups if cup not in removed_cups]
    
    ## The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
    destination_cup_label = current_cup_label-1
    while True:
        if destination_cup_label in cups:
            break
        else:
            destination_cup_label += -1
        
        if destination_cup_label < min(cups):
            destination_cup_label = max(cups)
            break
    
    ## The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
    destination_cup_index = cups.index(destination_cup_label)
    for removed_cup in reversed(removed_cups):
        cups.insert(destination_cup_index+1, removed_cup)
    
    ## The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    current_cup_index = (cups.index(current_cup_label)+1) % nr_cups
    return cups, current_cup_index

def get_results(cups):
    index_1 = cups.index(1)
    result_part1 = ''.join([str(cups[(index_1+i) % nr_cups]) for i in range(1,9)])
    result_part2 = cups[(index_1+1)%nr_cups] * cups[(index_1+2)%nr_cups]
    return result_part1, result_part2

def run(nr_cups, nr_of_moves, fun=step):
    print('')
    print(f'=== fun={fun.__name__} == nr_of_moves={nr_of_moves} == nr_cups={nr_cups} ===')

    cups = list(range(1, nr_cups+1))
    for i,c in enumerate(input):
        cups[i] = int(c)
    current_cup = 0
    
    tic = time.time()
    for i in tqdm(range(nr_of_moves), position=0, leave=False):
        cups, current_cup = fun(cups, current_cup)
    toc = time.time()
    
    result_part1, result_part2 = get_results(cups)
    print(f'result_part1={result_part1}, result_part2={result_part2}, time={toc-tic}s')
    return result_part1, result_part2


def step_links(links, current_cup):
    ## The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.    
    cup = current_cup
    removed_cups = []
    for i in range(3):
        cup = links[cup]
        removed_cups.append(cup)
    
    ## The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
    destination_cup = current_cup-1
    while 1:
        if destination_cup < 0:
            destination_cup = nr_cups-1
            
        if (destination_cup != removed_cups[0] 
            and destination_cup != removed_cups[1]
            and destination_cup != removed_cups[2]):
            break
        
        destination_cup -= 1

    ## The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
    links[current_cup], \
    links[destination_cup], \
    links[removed_cups[2]] = links[removed_cups[2]],\
                             links[current_cup],\
                             links[destination_cup]

    ## The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    current_cup = links[current_cup]
    return links, current_cup

def get_results_links(links):    
    result_part1 = []
    index = links[0]
    for i in range(0,8):
        result_part1.append(index+1)
        index = links[index]
    result_part1 = ''.join([str(i) for i in result_part1])
    result_part2 = (links[0]+1) * (links[links[0]]+1)
    return result_part1, result_part2

def run_links(nr_cups, nr_of_moves, fun=step_links):
    print('')
    print(f'=== fun={fun.__name__} == nr_of_moves={nr_of_moves} == nr_cups={nr_cups} ===')

    links = list(range(1, nr_cups+1))
    links[-1] = 0
    
    for i,c in enumerate(input):
        if i+1 < len(input):
            links[int(c)-1] = int(input[i+1])-1
        else:
            links[int(c)-1] = len(input)
    links[-1] = int(input[0])-1
    current_cup = int(input[0])-1
    
    tic = time.time()
    for i in tqdm(range(nr_of_moves), position=0, leave=False):
        links, current_cup = fun(links, current_cup)
    toc = time.time()
    
    result_part1, result_part2 = get_results_links(links)
    print(f'result_part1={result_part1}, result_part2={result_part2}, time={toc-tic}s')
    return result_part1, result_part2

def cups2links(cups):
    links = cups.copy()
    for i, c in enumerate(cups):
        if  i+1 < len(cups):
            links[c-1] = cups[i+1]-1
        else:
            links[c-1] = cups[0]-1
    return links

#### Compare step with step_links
nr_of_moves = 20
nr_cups = 12
run(nr_cups, nr_of_moves)
run_links(nr_cups, nr_of_moves)

#### Full run
nr_of_moves = 10000000
nr_cups = 1000000
run_links(nr_cups, nr_of_moves)