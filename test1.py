import numpy as np

def rss(y_real, y_predicted):
    squared_residuals = np.square(np.subtract(y_real, y_predicted))
    return sum(squared_residuals)

# создание массива данных, которые ложатся на логарифмическую кривую
x = np.array([1, 2, 3, 4, 5])
y_real = np.log(x) + np.random.normal(0, 0.1, size=5)

# расчет RSS на основе формулы, предсказывающей логарифмическую кривую
y_predicted = np.log(x)
print(rss(y_real, y_predicted))