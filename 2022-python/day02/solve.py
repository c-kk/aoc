lines = open("data.txt").read().split('\n')
rnds = [rnd.split(' ') for rnd in lines]

score = 0
for rnd in rnds:
    opp = rnd[0]
    you = rnd[1]
    shape_scores = {'X': 1 , 'Y': 2, 'Z': 3}

    score += shape_scores[you]

    if((opp == 'A' and you == 'Y') or (opp == 'B' and you == 'Z') or (opp == 'C' and you == 'X')): # win
        score += 6

    elif((opp == 'A' and you == 'X') or (opp == 'B' and you == 'Y') or (opp == 'C' and you == 'Z')): # draw
        score += 3

    else: # loss
        score += 0        

    #print(opp, you, score)

print(score)

score = 0
for rnd in rnds:
    opp = rnd[0]
    result = rnd[1]
    result_scores = {'X': 0 , 'Y': 3, 'Z': 6}
    loss_lookup = {'A': 'Z', 'B': 'X', 'C': 'Y'}
    draw_lookup = {'A': 'X', 'B': 'Y', 'C': 'Z'}
    win_lookup = {'A': 'Y', 'B': 'Z', 'C': 'X'}
    shape_scores = {'X': 1 , 'Y': 2, 'Z': 3}

    score += result_scores[result]

    if(result == 'X'): # loss
        you = loss_lookup[opp]

    elif(result == 'Y'): # draw
        you = draw_lookup[opp]

    else: # win
        you = win_lookup[opp]    

    score += shape_scores[you]

    print(opp, result, you, score)

print(score)
