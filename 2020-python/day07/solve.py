lines = open("2020/day7/data.txt").read().split('\n')

bags = dict()
for line in lines:  # bright olive bags contain
                    # 1 dark tan bag, 4 striped orange bags, 3 bright orange bags.
    [parent, childs] = line.split(' bags contain ')
    childs = childs.replace('.', '').replace(' bags', '').replace(' bag', '').split(', ')
    childs = [child.split(" ", 1)[1] for child in childs]
    bags[parent] = childs

def find_bags_by_child(child):
    found_bags = set()
    for parent, childs in bags.items():
       found = child in childs
       if found:
           found_bags.add(parent)
    return found_bags

# Search for all bags that have 'shiny gold' as child
# child = 'shiny gold'
# all_found_bags = []
found_bags = {'shiny gold'}

found_bags2 = found_bags.copy()
for child in found_bags:
    found_bags2.update(find_bags_by_child(child))

found_bags3 = found_bags2.copy()
for child in found_bags2:
    found_bags3.update(find_bags_by_child(child))

found_bags4 = found_bags3.copy()
for child in found_bags3:
    found_bags4.update(find_bags_by_child(child))

found_bags5 = found_bags4.copy()
for child in found_bags4:
    found_bags5.update(find_bags_by_child(child))

found_bags6 = found_bags5.copy()
for child in found_bags5:
    found_bags6.update(find_bags_by_child(child))

found_bags7 = found_bags6.copy()
for child in found_bags6:
    found_bags7.update(find_bags_by_child(child))

found_bags8 = found_bags7.copy()
for child in found_bags7:
    found_bags8.update(find_bags_by_child(child))

found_bags9 = found_bags8.copy()
for child in found_bags8:
    found_bags9.update(find_bags_by_child(child))

pass
