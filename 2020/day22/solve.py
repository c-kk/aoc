import k
import collections
import math
import sys
import re
import numpy as np
import copy
import time

def import_data():
    groups = open(f"data{sys.argv[1]}.txt").read().split('\n\n')
    p1 = [int(number) for number in groups[0].split('\n')[1:]]
    p2 = [int(number) for number in groups[1].split('\n')[1:]]
    return p1, p2

def calculate_score(p):
    length = len(p)
    rang = list(range(1, length + 1))[::-1]
    score = sum(map(np.prod, zip(p, rang)))
    return score

# Part 1
def play_game_part1(game, p1, p2):
    round = 0
    while True:
        if len(p1) == 0 or len(p2) == 0: break
        round += 1

        print(f"-- Round {round} (Game {game}) --")
        print(f"Player 1's deck: {p1}")
        print(f"Player 2's deck: {p2}")

        c1, c2 = p1.pop(0), p2.pop(0)
        print(f"Player 1 plays: {c1}")
        print(f"Player 2 plays: {c2}")

        if c1 > c2:
            print(f"Player 1 wins round {round} of game {game}!")
            p1.extend([c1, c2])
            if len(p2) == 0: break
        elif c2 > c1:
            print(f"Player 2 wins round {round} of game {game}!")
            p2.extend([c2, c1])
            if len(p1) == 0: break

        print('')

    if len(p2) == 0:
        print(f"Player 1 wins game {game}\n")
    elif len(p1) == 0:
        print(f"Player 2 wins game {game}\n")

    return p1, p2

# p1, p2 = import_data()
# p1, p2 = play_game_part1(1, p1, p2)
# print("== Post-game results ==")
# print(f"Player 1's deck: {p1}")
# print(f"Player 2's deck: {p2}")
# print('Answer 1:', calculate_score(p1 + p2), '\n\n')

# Part 2
def game_win_by_having_all_cards(game, p1, p2):
    if len(p1) == 0 or len(p2) == 0:
        if len(p2) == 0: 
            winner = 1
            score = calculate_score(p1)

        if len(p1) == 0: 
            winner = 2
            score = calculate_score(p2)

        print(f"Player {winner} wins game {game}\n")
        return winner, score
    return None, None

def game_win_by_same_cards_in_previous_round(history, game, p1, p2):
    if game in history:
        if [p1, p2] in history[game]:
            winner = 1
            score = calculate_score(p1)
            print(f"Player {winner} wins game {game}\n")
            return winner, score
    return None, None


def play_round(history, cache, game, p1, p2, rnd):
    new_p1 = copy.copy(p1)
    new_p2 = copy.copy(p2)

    print(f"== Game {game} - Round {rnd} ==")
    print(f"Player 1's deck: {new_p1}")
    print(f"Player 2's deck: {new_p2}")

    c1, c2 = new_p1.pop(0), new_p2.pop(0)
    print(f"Player 1 plays: {c1}")
    print(f"Player 2 plays: {c2}")

    remaining1 = len(new_p1)
    remaining2 = len(new_p2)
    if c1 <= remaining1 and c2 <= remaining2:
        print("Playing subgame...")
        subgame = max(history.keys()) + 1
        # if subgame > 100: exit()
        winner, score = play_game(history, cache, subgame, new_p1[0:c1], new_p2[0:c2])
        if winner == 1:
            print(f"Player 1 wins round {rnd} of game {game} by subgame {subgame}!")
            new_p1.extend([c1, c2])
        elif winner == 2:
            print(f"Player 2 wins round {rnd} of game {game} by subgame {subgame}!")
            new_p2.extend([c2, c1])

    elif c1 > c2:
        print(f"Player 1 wins round {rnd} of game {game}!")
        new_p1.extend([c1, c2])
    elif c2 > c1:
        print(f"Player 2 wins round {rnd} of game {game}!")
        new_p2.extend([c2, c1])

    print('')

    # time.sleep(1)
    return history, cache, game, new_p1, new_p2, rnd


def play_game(history, cache, game, p1, p2):
    new_p1 = copy.copy(p1)
    new_p2 = copy.copy(p2)

    print(f"\n== Game {game} ==")
    print(f"Player 1's deck: {new_p1}")
    print(f"Player 2's deck: {new_p2}")
    print("")

    rnd = 0
    while True:
        winner, score = game_win_by_having_all_cards(game, new_p1, new_p2)
        if winner: 
            print("Win by having all cards")
            return winner, score
        
        winner, score = game_win_by_same_cards_in_previous_round(history, game, new_p1, new_p2)
        if winner: 
            print("Win by same cards in previous round")
            return winner, score
        
        if game in history:
            history[game].append([new_p1, new_p2])
        else:
            history[game] = [[new_p1, new_p2]]

        rnd += 1

        cache_p1 = tuple(copy.copy(new_p1))
        cache_p2 = tuple(copy.copy(new_p2))

        if (cache_p1, cache_p2) in cache:
            [new_p1, new_p2] = cache[(cache_p1, cache_p2)]
            # print("Retreived from cache!")
            # exit()
        else:
            history, cache, game, new_p1, new_p2, rnd = play_round(history, cache, game, new_p1, new_p2, rnd)
            cache[(cache_p1, cache_p2)] = [new_p1, new_p2]
            # for ckey, cvalue in cache.items():
            #     print("Cache key", ckey)
            #     print("Cache value", cvalue)
        
# Part 2
p1, p2 = import_data()
history = {1: []}
cache = {}
winner, score = play_game(history, cache, 1, p1, p2)
print('Answer 2:', score)