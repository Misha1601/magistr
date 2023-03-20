from Basemodel import *
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')
print(data)
data = np.array(data)
print(data)
body = data[:, 1]
print(body)