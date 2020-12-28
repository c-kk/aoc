# Line import
lines = open(f"d{sys.argv[1]}.txt").read().split('\n')

# Group import and split
groups = open(f"d{sys.argv[1]}.txt").read().split('\n\n')
[rules, your_ticket, nearby_tickets] = [group.split('\n') for group in groups]

# Multiply inputs
def prod(factors):
	from functools import reduce
    return reduce(lambda a, b: a * b, factors, 1)