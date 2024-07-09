import numpy as np

def Gompertz3(x, B, C, M):
    """
    Функция расчета Prognose Sales с 3 переменными
    n: величина Prognose Cumulative за прошлый год.
    k: полная выроботка энергии в предыдущем году
    ct = – затраты на 1 кВт/ч в предыдущем году
    """
    data0 = x[0]
    n = x[1]
    k = x[2]
    ct = x[3]
    return data0 + (M / (M + ct)) * k * (np.exp(-np.exp(B - C * n)))

def squareMistakeGompertz3(k: tuple, sales, total, costs) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.
    k: кортеж начальных параметров (B, C, M);
    sales: кортеж Sales.
    """
    # Начальные значения для первого года
    res = 0  # Значение функции
    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        z = sales[0], i, total[i-1], costs[i-1]
        p = Gompertz3(z, k[0], k[1], k[2])  # Новый Prognose Sales
        res += (p - sales[i])**2  # Добавляем
    return res
