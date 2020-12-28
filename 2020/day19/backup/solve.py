import collections
import math
import re
import sys
import yaml
import copy

answer1 = 0
groups = open(f"data{sys.argv[1]}.txt").read().split('\n\n')
groups[0] = groups[0].replace("\"", "")
rules_input = groups[0].split('\n') # ['0: 4 1 5', '1: 2 3 | 3 2', '2: 4 4 | 5 5', '3: 4 5 | 5 4', '4: "a"', '5: "b"']
messages = groups[1].split('\n')
# print(rules_input, messages)

rules = dict()
for rule_input in rules_input:
	[index, rest] = rule_input.split(': ')
	index = int(index)
	groups = rest.split(' | ')
	groups = [group.split(' ') for group in groups]
	try:
		groups = [list(map(int, group)) for group in groups]
	except:
		pass
		# letter = groups[0]
		# groups = letter
	# print(groups)
	rules[index] = groups

max_key = max(rules.keys())
frules = copy.deepcopy(rules)
for key, rule in rules.items():
	print(key, rule)
	if(len(rule) == 1):
		frules[key] = rule[0]
	else:
		rule1 = rule[0]
		rule2 = rule[1]

		frules[key] = rule1

		max_key += 1
		rule2_key = max_key
		frules[rule2_key] = rule2

		# rules_using_key = [rule for rule in frules if key in rule]
		found_keys = [fkey for fkey in frules if key in frules[fkey]]
		print("-", found_keys) 

		for found_key in found_keys:
			old_rule = frules[found_key]
			extra_rule = [x if x != key else rule2_key for x in old_rule]
			
			max_key += 1
			frules[max_key] = extra_rule
			print("--", extra_rule)

print('\n')
for key, rule in frules.items():
	print(key, rule)


def parse(rule):
	new_rule = []
	for item in rule:
		# print(item)
		if isinstance(item, str):
			new_rule.append(item)
		else:
			lookup = frules[item]
			parsed = parse(lookup)
			new_rule.append(*parsed)


	# print(new_rule)
	# are_all_strings = all([isinstance(item, str) for item in new_rule])
	# if are_all_strings:
	print(new_rule)
	new_rule = [''.join(new_rule)]
	return new_rule

rule = frules[7]
print(rule)
parsed = parse(rule)
print(parsed)
