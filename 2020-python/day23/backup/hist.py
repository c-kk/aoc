import copy

def last_seen_at(history, arrangement):
	arr = tuple(arrangement)
	return history.get(arr, None)

def add_to_history(history, arrangement, move):
	arr = tuple(arrangement)
	history[arr] = move
	return history