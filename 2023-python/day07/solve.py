data_version = input("Data version (1 or 2): ")
filename = "data1.txt" if data_version != "2" else "data2.txt"
lines = open(filename).read().split('\n')
# for line in lines:
#     print(line)

# Part 1
print("*** Part 1 ***")
score_part1 = 0

def get_hand_value_part_1(hand):
    hand_value = 0
    for card_index, card in enumerate(hand):
        if card_index == 0:
            hand_value += card * 14 * 14 * 14 * 14
        elif card_index == 1:
            hand_value += card * 14 * 14 * 14
        elif card_index == 2:
            hand_value += card * 14 * 14
        elif card_index == 3:
            hand_value += card * 14
        elif card_index == 4:
            hand_value += card

    cards_found = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for card in hand:
        cards_found[card] += 1

    if 5 in cards_found:
        hand_value += 6000000
    elif 4 in cards_found:
        hand_value += 5000000
    elif 3 in cards_found and 2 in cards_found:
        hand_value += 4000000
    elif 3 in cards_found and 2 not in cards_found:
        hand_value += 3000000
    elif cards_found.count(2) == 2:
        hand_value += 2000000
    elif cards_found.count(2) == 1:
        hand_value += 1000000

    print('Hand:', hand, 'Cards found:', cards_found, 'Hand value:', hand_value)
    return hand_value

card_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
hand_and_bids = [[[card_dict.get(char) for char in line.split(' ')[0]], int(line.split(' ')[1])] for line in lines]

hand_and_bids_sorted = sorted(hand_and_bids, key=lambda x: get_hand_value_part_1(x[0]))
for hand_and_bid in hand_and_bids_sorted:
    print(hand_and_bid)

for hand_and_bid_index, hand_and_bid in enumerate(hand_and_bids_sorted):
    bid = hand_and_bid[1]
    score_part1 += bid * (hand_and_bid_index + 1)

print("Score part 1:", score_part1)

# Part 2
print("*** Part 2 ***")
score_part2 = 0

def get_hand_value_part_2(hand):
    hand_value = 0
    for card_index, card in enumerate(hand):
        if card_index == 0:
            hand_value += card * 14 * 14 * 14 * 14
        elif card_index == 1:
            hand_value += card * 14 * 14 * 14
        elif card_index == 2:
            hand_value += card * 14 * 14
        elif card_index == 3:
            hand_value += card * 14
        elif card_index == 4:
            hand_value += card

    cards_found = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for card in hand:
        cards_found[card] += 1

    jokers = cards_found[1]
    cards_found[1] = 0 # Reset jokers
    cards_found[cards_found.index(max(cards_found))] += jokers

    if 5 in cards_found:
        hand_value += 6000000
    elif 4 in cards_found:
        hand_value += 5000000
    elif 3 in cards_found and 2 in cards_found:
        hand_value += 4000000
    elif 3 in cards_found and 2 not in cards_found:
        hand_value += 3000000
    elif cards_found.count(2) == 2:
        hand_value += 2000000
    elif cards_found.count(2) == 1:
        hand_value += 1000000

    print('Hand:', hand, 'Cards found:', cards_found, 'Hand value:', hand_value)
    return hand_value

card_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
hand_and_bids = [[[card_dict.get(char) for char in line.split(' ')[0]], int(line.split(' ')[1])] for line in lines]

hand_and_bids_sorted = sorted(hand_and_bids, key=lambda x: get_hand_value_part_2(x[0]))
for hand_and_bid in hand_and_bids_sorted:
    print(hand_and_bid)

for hand_and_bid_index, hand_and_bid in enumerate(hand_and_bids_sorted):
    bid = hand_and_bid[1]
    score_part2 += bid * (hand_and_bid_index + 1)

print("Score part 2:", score_part2)

print("*** Scores ***")
print("Score part 1:", score_part1)
print("Score part 2:", score_part2)