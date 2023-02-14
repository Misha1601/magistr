import pandas as pd
import cvxpy as cp
import numpy as np
#import gdown

df = pd.read_csv('flight_schedule.csv', index_col=0, header=1)
schedule = df.iloc[:-2]
cost = df.iloc[-2]
hours = df.iloc[-1]
# print(df)

schedule = schedule.applymap(lambda x: 1 if x >= 1 else x)
# print(schedule)

a = schedule.values
# print(a)
c = cost.values
# print(c)
b = np.ones(len(a))
print(b)

y = cp.Variable(len(c), boolean=True)

constraints = [a @ y >= b]

obj = cp.Minimize(c @ y)
prob = cp.Problem(obj, constraints)
prob.solve() #solver=cp.GLPK_MI)

# print(prob.status)
# print(y.value)

h = hours.values
# print(h)

constraints = [a @ y >= b, h @ y <= 1700]
prob = cp.Problem(obj, constraints)
prob.solve() # solver=cp.GLPK_MI())

# print(y.value)