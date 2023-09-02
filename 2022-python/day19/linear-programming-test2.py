import numpy as np
from copy import copy, deepcopy
from pulp import *
import timeit

# Inputs
t = 24
robots = ["ore","clay","obsidian","geode"]

#Blueprint 0: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
robot_cost = {
    "ore" : [2, 0, 0, 0],
    "clay" : [3, 0, 0, 0],
    "obsidian" : [3, 8, 0, 0],
    "geode" : [3, 0, 12, 0],
}

#Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 4 ore and 11 obsidian.
# robot_cost = {
#     "ore" : [4, 0, 0, 0],
#     "clay" : [4, 0, 0, 0],
#     "obsidian" : [3, 7, 0, 0],
#     "geode" : [4, 0, 11, 0],
# }

#Blueprint 2: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 2 ore and 20 obsidian.
# robot_cost = {
#     "ore" : [3, 0, 0, 0],
#     "clay" : [3, 0, 0, 0],
#     "obsidian" : [2, 20, 0, 0],
#     "geode" : [2, 0, 20, 0],
# }

#Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 8 obsidian.
#robot_cost = {
#    "ore" : [4, 0, 0, 0],
#    "clay" : [4, 0, 0, 0],
#    "obsidian" : [3, 14, 0, 0],
#    "geode" : [4, 0, 8, 0],
#}


robot_production = {
    "ore" : [1, 0, 0, 0],
    "clay" : [0, 1, 0, 0],
    "obsidian" : [0, 0, 1, 0],
    "geode" : [0, 0, 0, 1],
}

time = range(1,t+1)
robot_buy_at_t = [(r,t) for t in time for r in robots]
# vars is choose to buy robot r at time t or not
vars = LpVariable.dicts("Choice", robot_buy_at_t, cat="Binary")

# Express production in terms of the buy choice
production_at_t = np.full((t+1, 4), None)
production_at_t[0] = [0, 0, 0, 0]
production_at_t[1] = [1, 0, 0, 0]
for t in time[1:]:
  for i in range(4):
    production_at_t[t,i] = copy(production_at_t[t-1,i])
    for r in robots:
      production_at_t[t][i] += robot_production[r][i]*vars[r,t-1]
#print("============== production_at_t ==============")
#display(production_at_t)

# Express stock in terms of the buy choice
stock_at_t_after_buy = np.full((t+1, 4), None)
stock_at_t_after_buy[0] = [0, 0, 0, 0]
for t in time:
  for i in range(4):
    stock_at_t_after_buy[t,i] = stock_at_t_after_buy[t-1,i] + production_at_t[t-1][i]
    for r in robots:
      stock_at_t_after_buy[t,i] += -robot_cost[r][i]*vars[r,t]
#print("============== stock_at_t_after_buy ==============")
#display(stock_at_t_after_buy)

# Initialize solver
prob = LpProblem("Robot_Problem", sense = const.LpMaximize)

# Goal
prob += (
    stock_at_t_after_buy[-1, -1] + production_at_t[-1, -1],
    "Stock_geode_at_end",
)

# Constraint 1 - Stock not negative
for t in time:
  for i in range(4):
    prob += (stock_at_t_after_buy[t,i] >= 0, f"Stock_t{t}_i{i}")

# Constraint 2 - One robot at the time
for t in time:
  c = 0
  for r in robots:
    c += vars[r,t]
  prob += c >= 0
  prob += c <= 1

# Solve
prob.solve()
print("============== result ==============")
print("Status:", LpStatus[prob.status])
print("Score:", value(prob.objective))

print(f"{'time':<10}", end="")
for t in time:
  print(t%10, end="")
print("")
for r in robots:
  print(f"{r:<10}", end="")
  for t in time:
    print(1 if value(vars[r,t]) >0 else 0, end="")
  print("")