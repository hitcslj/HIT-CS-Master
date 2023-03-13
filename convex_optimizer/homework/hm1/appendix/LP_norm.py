'''
用来偷懒的,验证最优解是否正确
pip install pulp
'''

from pulp import *

# 定义问题
prob = LpProblem("Linear Programming Problem", LpMaximize)

# 定义变量
x1 = LpVariable("x1", lowBound=0)
x2 = LpVariable("x2", lowBound=0)
x3 = LpVariable("x3", lowBound=0)
# x4 = LpVariable("x4", lowBound=0)
# x5 = LpVariable("x5", lowBound=0)
# x6 = LpVariable("x6", lowBound=0)
# x7 = LpVariable("x7", lowBound=0)

# 定义目标函数
# prob += (-2*x1+x2-x3-x4+x5)
prob += 4*x1+2*x2+8*x3

# 定义约束条件
# prob += (2*x1+3*x2+5*x3 == 8)
# prob += (x1-x2+x3+x4-x5+x6 == 7)
# prob += (x1-2*x3+2*x4-2*x5-x7 == 1)
prob += 2*x1-x2+3*x3<= 30
prob += x1+2*x2+4*x3 == 40


# 求解问题
status = prob.solve()

# 打印结果
print("Status:", LpStatus[status])
print("Optimal Value:", value(prob.objective))
print("Optimal Solution:")
for var in prob.variables():
    print(var.name, "=", var.value())

