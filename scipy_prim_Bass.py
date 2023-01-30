import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                     'generation': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]})
data['cum_sum'] = data['generation'].cumsum()
print(data)

def c_t(x, p, q, m):
    return (p+(q/m)*(x))*(m-x)
popt, pcov = curve_fit(c_t, data.cum_sum[0:11], data.generation[1:12], maxfev=800)
print(popt)

p = [popt[0]]*26
q = [popt[1]]*26
m = [popt[2]]*26

prog = map(c_t, data.year, p, q, m)
prog1 = list(prog)
# print(prog1)

# print(len(data.year))
# print(len(prog1))
data['prog'] = prog1
data['prog_sum'] = data['prog'].cumsum()
print(data)

plt.plot(data.year, data.generation, 'b-', label='generation')

# popt1 = [0.0005727, 0.249517965, 2407.09678]
# print(popt1)
# plt.plot(data.year, c_t(data.year, *popt), 'r-')
plt.plot(data.year, data.prog_sum, 'r-')

plt.xlabel('year')
plt.ylabel('generation')
plt.legend()
plt.show()