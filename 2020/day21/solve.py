import sys
import re
import time
import copy

lines = open(f"data{sys.argv[1]}.txt").read().split('\n')
print(lines)
print('\n')

# 'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)'
rules = []
all_words = []
all_ws = set()
all_als = set()

for line in lines:
	ws, als = re.split("\ \(contains ", line)
	ws = ws.split(' ')
	als = als.replace(')', '')
	als = als.split(', ')

	rule = [ws, als]
	rules.append(rule)

	for w in ws:
		all_ws.add(w)
		all_words.append(w)

	for al in als:
		all_als.add(al)

print('Rules')
for rule in rules: print(rule)
print('')
print('All words', all_ws)
print('All allergics', all_als)
print('')

als_dict = dict()
for al in all_als:
	als_dict[al] = list(all_ws)

for rule_ws, rule_als in rules:
	print('Rule')
	print(rule_ws, rule_als)
	print('')

	print('Allergics dict - start')
	for key, line in als_dict.items(): print(key, line)
	print('')

	for al, ws in als_dict.items():
		new_candidates = copy.copy(ws)
		for current_candidate in ws:
			if al in rule_als and current_candidate not in rule_ws:
				print(f"A. Removing {current_candidate} from {al} because {al} in rule and {current_candidate} not in rule")
				new_candidates.remove(current_candidate)
		als_dict[al] = new_candidates

	print('')
	print('Allergics dict - result')
	for key, line in als_dict.items(): print(key, line)
	print('\n')

allergic_words = set([word for words in als_dict.values() for word in words])
print(allergic_words)

none_allergic_words = list(all_ws - set(allergic_words))
print(none_allergic_words)

occurences = [all_words.count(word) for word in none_allergic_words]
print(sum(occurences))

allergics = {
	'mfqgx': 'soy',
	'cdqvp': 'dairy',
	'rffqhl': 'wheat',
	'zhqjs': 'fish',
	'tgmzqjz': 'shellfish',
	'rbpg': 'peanuts',
	'xvtrfz': 'sesame',
	'dglm': 'eggs',
}

# cdqvp': 'dairy',
# dglm': 'eggs',
# zhqjs': 'fish',
# rbpg': 'peanuts',
# xvtrfz': 'sesame',
# tgmzqjz': 'shellfish',
# mfqgx': 'soy',
# rffqhl': 'wheat',

# cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl

