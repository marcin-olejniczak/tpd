from pulp import *

# declare your variables
x1 = LpVariable("x1", 0, 1)  # 0<= x1 <= 40
x2 = LpVariable("x2", 0, 1)  # 0<= x2 <= 1000

# defines the problem
prob = LpProblem("problem", LpMinimize)

# defines the constraints
prob += (5 * x1) + (2 * x2) >= 1
prob += (0 * x1) + (4 * x2) >= 1
prob += (1 * x1) + (3 * x2) >= 1

#prob += x1 > 0 these 2 conditions are probably not necessary
#prob += x2 > 0

# defines the objective function to maximize
prob += x1 + x2

# solve the problem
status = prob.solve(GLPK(msg=0))
LpStatus[status]

# print the results x1 = 20, x2 = 60
x1 = value(x1)
x2 = value(x2)

print "X1':{},X2':{},".format(
    x1, x2,
)

v = 1 / (x1 + x2)
f1 = x1 * v
f2 = x2 * v
print 'V:{}, X1:{}, X2:{}'.format(
    v, f1, f2,
)