lines = open("2020/day7/data.txt").read().split('\n')

bags = dict()
for line in lines:  # bright olive bags contain
                    # 1 dark tan bag, 4 striped orange bags, 3 bright orange bags.
    [parent, childs] = line.split(' bags contain ')
    childs = childs.replace('.', '').replace(' bags', '').replace(' bag', '').split(', ')
    childs = [child.split(" ", 1) for child in childs]
    bags[parent] = childs

def amount_of_children(_bag):
    _count = 1
    for [_amount, _child_name] in _bag:
        if _amount == 'no': return 1
        _child = bags[_child_name]
        _count += int(_amount) * amount_of_children(_child)
    return _count

bag = bags['shiny gold']
count = amount_of_children(bag)
pass

# 85325 - too high
# 16894 - too low
# 85324 - right