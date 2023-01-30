from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
#time intervals
t= np.array([1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
# sales vector
sales=np.array([8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193])
# cumulatice sales
c_sales=np.cumsum(sales)
# initial variables(M, P & Q)
vars = [2407.09677988243, 0.0005727, 0.249517965]

# residual (error) function
def residual(vars, t, sales):
    M = vars[0]
    P = vars[1]
    Q = vars[2]
    Bass = M * (((P+Q)**2/P)*np.exp(-(P+Q)*t))/(1+(Q/P)*np.exp(-(P+Q)*t))**2
    return (Bass - (sales))

# non linear least square fitting
varfinal,success = leastsq(residual, vars, args=(t, sales))

# estimated coefficients
m = varfinal[0]
p = varfinal[1]
q = varfinal[2]


print(varfinal)
#sales plot (pdf)
#time interpolation
tp=t# (np.linspace(1.0, 100.0, num=100))/10
cofactor= np.exp(-(p+q) * tp)
sales_pdf= m* (((p+q)**2/p)*cofactor)/(1+(q/p)*cofactor)**2
plt.plot(tp, sales_pdf,t,sales)
plt.title('Sales pdf')
plt.legend(['Fit', 'True'])
plt.show()


# Cumulative sales (cdf)
sales_cdf= m*(1-cofactor)/(1+(q/p)*cofactor)
plt.plot(tp, sales_cdf,t,c_sales)
plt.title('Sales cdf')
plt.legend(['Fit', 'True'])
plt.show()