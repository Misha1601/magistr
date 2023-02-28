import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                     'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]})
data['cum_sum'] = data['generate'].cumsum()
# print(data)

x = np.array([])
y = np.array([])
# print(x)
# x = np.append(x, [0])
for i in range(len(data.year[0:-1])):
    # x = np.append(x, 0)
    x = np.append(x, np.linspace(data.year[i], data.year[i+1], 5))
    for n in x[-5:]:
        y = np.append(y, np.random.uniform(data.generate[i], data.generate[i+1]))
# print(x)
# print(y)
# print(len(x))
# print(len(y))
data1 = pd.DataFrame({'year': x,
                     'generate': y})
data1['cum_sum'] = data1['generate'].cumsum()
print(data1)
# Оптимизируя идеальные значения p, q и m, получаем
def func(x, p, q, m):
#     return (p+(q/m)*(x))*(m-x)
    return (p*m+(q-p)*(x))-(q/m)*(x**2)

plt.plot(x, y, 'b-', label='generation')

popt, pcov = curve_fit(func, data1.cum_sum, data1.generate, maxfev = 10000)
plt.plot(x, func(data1.cum_sum, *popt), 'r-',
# plt.plot(x, func(x, 0.000572584736024431, 0.249521951557201, 2407.09431915446), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
print(*popt)

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()