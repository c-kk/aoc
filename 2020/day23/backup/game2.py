import copy

def pick_cups(arra, curr):
	curr_idx = arra.index(curr)
	cups = []
	for i in range(1, 4):
		pick_idx = (curr_idx + i) % len(arra)
		cup = arra[pick_idx]
		cups.append(cup)
	return cups

def remo_cups(arra, cups):
	for cup in cups:
		arra.remove(cup)
	return arra

def pick_dest(arra, curr):
	dest = curr - 1
	while True:
		if dest < min(arra): dest = max(arra)
		if dest in arra: return dest
		dest -= 1
	
def plac_cups(arra, cups, dest):
	dest_idx = arra.index(dest)
	for i, cup in enumerate(cups):
		arra.insert(dest_idx + 1 + i, cup)
	return arra

def pick_curr(arra, curr):
	curr_idx = arra.index(curr)
	new_curr_idx = (curr_idx + 1) % len(arra)
	new_curr = arra[new_curr_idx]
	return new_curr
