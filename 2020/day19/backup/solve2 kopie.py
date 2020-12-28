import sys
import copy

groups = open(f"data{sys.argv[1]}.txt").read().split('\n\n')
rs = groups[0].split('\n')
messages = groups[1].split('\n')

# rs ['0:4,1,5', '1:2,3|3,2', '2:4,4|5,5', '3:4,5|5,4', '4:a', '5:b']
rules = dict()
for r in rs:
	key, rest = r.split(':')
	groups = []
	for group in [group.split(',') for group in rest.split('|')]:
		groups.append([int(char) if char.isdigit() else char for char in group])
	rules[int(key)] = groups
print(rules)

# rules 0: [[4, 1, 5]], 1: [[2, 3], [3, 2]], 2: [[4, 4], [5, 5]], 3: [[4, 5], [5, 4]], 4: [[a]], 5: [[b]]
# rules 0: [[4, 1, b]], 1: [[2, 3], [3, 2]], 2: [[4, 4], [b, b]], 3: [[4, b], [b, 4]], 4: [[a]]
# rules 0: [[4, 1, b]], 1: [[2, 3], [3, 2]], 2: [[4, 4], [bb]], 3: [[4, b], [b, 4]], 4: [[a]]
# rules 0: [[a, 1, b]], 1: [[2, 3], [3, 2]], 2: [[a, a], [b, b]], 3: [[a, b], [b, a]]
# rules 0: [[a, 1, b]], 1: [[2, 3], [3, 2]], 2: [[aa], [bb]], 3: [[ab], [ba]]
# rules 0: [[a, 1, b]], 1: [[2, ab], [2, ba], [ab, 2], [ba, 2]], 2: [[aa], [bb]]
# rules 0: [[a, 1, b]], 1: [[aa, ab], [bb, ab], [aa, ba], [bb, ba], [ab, aa], [ab, bb], [ba, aa], [ba, bb]]
# rules 0: [[a, 1, b]], 1: [[aaab], [bbab], [aaba], [bbba], [abaa], [abbb], [baaa], [babb]]
# rules 0: [[a, aaab, b], [a, bbab, b], [a, aaba, b], [a, bbba, b], [a, abaa, b], [a, abbb, b], [a, baaa, b], [a, babb, b]]
# rules 0: [[aaaabb], [abbabb], [aaabab], [abbbab], [aabaab], [aabbbb], [abaaab], [ababbb]]

def select_replace_join(rules):
	# Select the rule with only strings
	selected_key = None
	for rule_key, rule in rules.items():
		all_string = all([isinstance(item, str) for group in rule for item in group])
		if all_string:
			selected_key, selected_rule = rule_key, rule
			# print("Selected", selected_key, selected_rule)
			break		
	
	if not selected_key:
		print("No rule found with all strings")
		for rule in rules.values():
			for group in rule:
				print(group)
		print(f'Rule 8: {rules[8]} \n')
		print(f'Rule 11: {rules[11]} \n')
		print(f'Rule 42: {rules[42]} \n')
		print(f'Rule 31: {rules[31]} \n')
		# 	print(group)
		# print(rules[0])
		exit()
		return rules

	# Find the selected_key in other rules and replace it with the selected rule
	for rule_key, rule in rules.items():
		for group_key, group in enumerate(rule):
			for item_key, item in enumerate(group):
				if item == selected_key:					
					rules[rule_key][group_key][item_key] = selected_rule[0][0]
					for select_group_index, selected_group in enumerate(selected_rule[1:]):
						new_group = copy.copy(rules[rule_key][group_key])
						new_group[item_key] = selected_group[0]
						rules[rule_key].append(new_group)
	del(rules[selected_key])
	print(rules)

	# Join string characters in groups with all strings
	for rule_key, rule in rules.items():
		for group_key, group in enumerate(rule):
			all_string = all([isinstance(item, str) for item in group])
			if all_string:
				rules[rule_key][group_key] = ["".join(group)]
	for group in rules[0]: print(group)
	print(f'Count: {len(rules[0])}')
	return rules

while len(rules) > 1:
	rules = select_replace_join(rules)

valid_messages = [group[0] for group in rules[0]]
valid = sum([message in valid_messages for message in messages])
print(valid)
