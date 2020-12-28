import re
import copy
import time

def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

groups = open(f"data1.txt").read().split('\n\n')
[rules, your_ticket, nearby_tickets] = [group.split('\n') for group in groups]

# ['departure location', '48', '793', '800', '971']
rules = [split([': ', '-', ' or '], rule) for rule in rules]

# [157, 59, 163, 149, 83, 131, 107, 89, 109, 113, 151, 53, 127, 97, 79, 103, 101, 173, 167, 61]
your_ticket = [int(number) for number in your_ticket[1].split(',')]

# [[946, 293, 123, 156, 812, 202, 75, 884, 162, 420, 436, 60, 720, 719, 272, 642, 515, 724, 150, 875], ...]
nearby_tickets = [[int(number) for number in nearby_ticket.split(',')] for nearby_ticket in nearby_tickets[1:]]

all_ranges = [int(number) for rule in rules for number in rule[1:]]
all_ranges = list(zip(all_ranges[::2], all_ranges[1::2]))

# all_values = [number for ticket in nearby_tickets for number in ticket]

valid_tickets = []
for ticket in nearby_tickets:
	is_valid_ticket = True
	for value in ticket:
		is_valid_value = False
		for (minimum, maximum) in all_ranges:
			if minimum <= value <= maximum:
				is_valid_value = True
		if not is_valid_value:
			is_valid_ticket = False
	if is_valid_ticket:
		valid_tickets.append(ticket)

# print(len(valid_tickets))

values_per_column = []
for index in range(len(rules)):
	values = [ticket[index] for ticket in valid_tickets]
	values_per_column.append(values)

possible_rules_per_column = []
for column_index, values in enumerate(values_per_column):
	possible_rules = []
	for rule in rules:
		is_possible_rule = True
		for value in values:
			[rule_name, min1, max1, min2, max2] = rule
			is_valid_value = int(min1) <= value <= int(max1) or int(min2) <= value <= int(max2)
			if not is_valid_value:
				is_possible_rule = False
		if is_possible_rule:
			possible_rules.append(rule_name)
			# print(possible_rules)
			# print(values)
			# exit()
	possible_rules_per_column.append(possible_rules)

# print(rules)
# print(*possible_rules_per_column, sep='\n')

while True:
	found_rule_name = None
	for key, rule_names in enumerate(possible_rules_per_column):
		if len(rule_names) == 1 and sum([rule_names[0] in rn for rn in possible_rules_per_column]) > 1:
			found_rule_name = rule_names[0]
			found_at_key = key
	if found_rule_name:
		rules_per_column = [[rule_name for rule_name in rule_names if rule_name != found_rule_name] for rule_names in possible_rules_per_column]
		rules_per_column[found_at_key] = [found_rule_name]
		possible_rules_per_column = rules_per_column
	else:
		break

print(possible_rules_per_column)


answer = 1
for index, [rule_name] in enumerate(possible_rules_per_column):
	if rule_name.startswith('departure'):
		print(index, rule_name, your_ticket[index])
		answer *= your_ticket[index]
print(answer)
