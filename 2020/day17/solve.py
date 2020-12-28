lines = open(f"data1.txt").read().split('\n')

actives = set()
y = 0
z = 0
for line in lines:
	x = 0
	for char in line:
		if char == '#':
			actives.add((x, y, z))
		x += 1
	y += 1

for cycle in range(6):
	new_actives = set()

	zs = [z for (x, y, z) in actives]
	ys = [y for (x, y, z) in actives]
	xs = [x for (x, y, z) in actives]

	for z in range(min(zs) - 1, max(zs) + 2):
		for y in range(min(ys) - 1, max(ys) + 2):
			for x in range(min(xs) - 1, max(xs) + 2):
				is_active = (x, y, z) in actives
				active_neighbours = 0	

				for z2 in range(z - 1, z + 2):
					for y2 in range(y - 1, y + 2):
						for x2 in range(x - 1, x + 2):
							if (x, y, z) == (x2, y2, z2):
								continue

							if (x2, y2, z2) in actives:
								active_neighbours += 1	
				
				print(cycle, x, y, z, "Active neighbours", active_neighbours)

				if is_active and 2 <= active_neighbours <= 3:
					new_actives.add((x, y, z))

				if not is_active and active_neighbours == 3:
					new_actives.add((x, y, z))

	actives = new_actives

print(len(actives))