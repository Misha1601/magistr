# Задание №6. Методом целочисленного программирования решить задачу:
# В цехе предприятия решено установить дополнительное оборудование, для размещения которого выделено 6 м2 площади. На приобретение оборудования предприятие может израсходовать 10 тыс. руб., при этом оно может купить оборудование двух видов. Комплект оборудования I вида стоит 1000 руб., а II вида – 3000 руб. Приобретение одного комплекта оборудования I вида позволяет увеличить выпуск продукции в смену на 2 ед., а одного комплекта оборудования II вида – на 4 ед. Зная, что для установки одного комплекта оборудования I вида требуется 2 м2 площади, а оборудования II вида – 1 м2 площади определить такой набор дополнительного оборудования, которых дает возможность максимально увеличить выпуск продукции.

import numpy as np
from scipy.optimize import linprog

# Коэффициенты целевой функции для минимизации (максимизации -2x - 4y)
c = np.array([-2, -4])

# Левые части ограничений
A = np.array([
    [2, 1],      # Ограничение площади
    [1000, 3000]  # Ограничение бюджета
])

# Правые части ограничений
b = np.array([6, 10000])

# Границы переменных (x и y)
x_bounds = (0, None)  # x >= 0
y_bounds = (0, None)  # y >= 0

# Решение с помощью целочисленного программирования
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Получение оптимальных значений x и y
x_optimal = res.x[0]
y_optimal = res.x[1]

# Максимальное значение целевой функции (-Z)
max_Z = -res.fun

print("Оптимальное количество оборудования I вида (x):", x_optimal)
print("Оптимальное количество оборудования II вида (y):", y_optimal)
print("Максимальное значение целевой функции (Z):", max_Z)
