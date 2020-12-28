import sys
import re
import collections
import math
import numpy as np

groups = open(f"d{sys.argv[1]}.txt").read().split('\n\n')
c1 = [int(c) for c in groups[0].split('\n')[1:]]
c2 = [int(c) for c in groups[1].split('\n')[1:]]

while True:
	print("c1", c1, "c2", c2)

	if len(c1) == 0 or len(c2) == 0:
		break

	p1 = c1.pop(0)
	p2 = c2.pop(0)
	print(p1, p2)

	if p1 > p2:
		c1.append(p1)
		c1.append(p2)
	else:
		c2.append(p2)
		c2.append(p1)

print("Finished")
print("c1", c1, "c2", c2)

summed = sum(map(np.product, zip(c1 + c2, [i for i in range(len(c1 + c2), 0, -1)])))
print(summed)

# multiplied = ()
