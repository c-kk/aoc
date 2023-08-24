from scipy.optimize import linprog

# Function: cost = 1x + 2y
cost_fun = [1, 2]

# Constraints
cons_left = []
cons_right = []

# Constraint 1: 1x + 1y ≤ 5
cons_left.append([1, 1])
cons_right.append(5)

# Constraint 2: 2x + 1y ≤ 10
cons_left.append([2, 1])
cons_right.append(10)

# Bound 1: x ≥ 2
x_bounds = (2, None) 

# Bound 2: y ≥ 1
y_bounds = (1, None) 

# Solve the problem
result = linprog(cost_fun, A_ub=cons_left, b_ub=cons_right, bounds=[x_bounds, y_bounds], method='highs')

# Print the result
print(result.message)
print(result.x, result.fun)