def Bass1(x: float, P: float, Q: float, M: float) -> float:
    """
    Функция расчета Prognose Sales с 1 переменной
    x: предыдущий прогноз, где y0 первое фактическое сгенерированное
    """
    return (P*M+(Q-P)*(x))-(Q/M)*(x**2)

def squareMistakeBass1(k: tuple, sales) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.
    k: кортеж начальных параметров (P, Q, M);
    sales: кортеж Sales.
    """
    c = sales[0]  # Начальный Prognose Cumulative
    res = 0  # Значение функции
    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        p = Bass1(c, k[0], k[1], k[2])  # Новый Prognose Sales
        c = c + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем
    return res

def Bass2(x, P, Q, K) -> float:
    """
    Функция расчета Prognose Sales с 2 переменными
    y = Y(t-1) сумма предыдущих прогнозов, где y0 первое фактическое сгенерированное
    m = М(t-1) общая генерация электроэнергии в предыдущий период за год
        """
    m = x[0]
    y = x[1]
    return (P * m * K + (Q - P) * y - (Q / (m * K) * y ** 2))

def squareMistakeBass2(k: tuple, sales, total) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.
    k: кортеж начальных параметров (P, Q, K);
    sales: кортеж Sales.
    """
    c = sales[0]  # Начальный Prognose Cumulative
    res = 0  # Значение функции
    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        z = total[i-1], c
        p = Bass2(z, k[0], k[1], k[2])  # Новый Prognose Sales
        c = c + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем
    return res

def Bass3(x, P, Q, K) -> float:
    """
    Функция расчета Prognose Sales с 3 переменными
    y = Y(t-1) сумма предыдущих прогнозов, где y0 первое фактическое сгенерированное
    m = М(t-1) общая генерация электроэнергии в предыдущий период за год
    ct = – затраты на 1 кВт/ч в предыдущем году
        """
    m = x[0]
    y = x[1]
    ct = x[2]
    return (P * (K / (K + ct)) * m + (Q - P) * y - (Q / ((K / (K + ct)) * m)) * y**2)

def squareMistakeBass3(k: tuple, sales, total, costs) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.
    k: кортеж начальных параметров (P, Q, K);
    sales: кортеж Sales.
    """
    c = sales[0]  # Начальный Prognose Cumulative
    res = 0  # Значение функции
    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        z = total[i-1], c, costs[i-1]
        p = Bass3(z, k[0], k[1], k[2])  # Новый Prognose Sales
        c = c + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем
    return res

import numpy as np

def Logic1(x, B, C, M) -> float:
    """
    Функция расчета Prognose Sales с 1 переменной
    n: величина Prognose Cumulative за прошлый год.
    """
    data0 = x[0]
    n = x[1]
    return data0 + (M) * (1/(1+np.exp(-B * (n - C))))

def squareMistakeLogic1(k: tuple, sales) -> float:
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
            p = Logic1((sales[0], i), k[0], k[1], k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res

import numpy as np

def Logic2(x, B, C, M) -> float:
    """
    Функция расчета Prognose Sales с 2 переменными
    n: величина Prognose Cumulative за прошлый год.
    k: полная выроботка энергии в предыдущем году
    """
    data0 = x[0]
    n = x[1]
    k = x[2]
    return data0 + (M * k) * (1/(1+np.exp(-B * (n - C))))

def squareMistakeLogic2(k: tuple, sales, total) -> float:
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
            z = sales[0], i, total[i-1]
            p = Logic2(z, k[0], k[1], k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res

import numpy as np

def Logic3(x, B, C, M) -> float:
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
    return data0 + (M/(M+ct)) * k * (1/(1+np.exp(-B * (n - C))))

def squareMistakeLogic3(k: tuple, sales, total, costs) -> float:
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
        p = Logic3(z, k[0], k[1], k[2])  # Новый Prognose Sales
        res += (p - sales[i])**2  # Добавляем
    return res

import numpy as np

def Gompertz1(x, B, C, M) -> float:
        """
        Функция расчета Prognose Sales
        x: величина Prognose Cumulative за прошлый год.
        """
        data0 = x[0]
        n = x[1]
        return data0 + (M) * (np.exp(-np.exp(B - C * n)))

def squareMistakeGompertz1(k: tuple, sales) -> float:
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
            p = Gompertz1((sales[0], i), k[0], k[1], k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res

import numpy as np

def Gompertz2(x, B, C, M) -> float:
    """
    Функция расчета Prognose Sales с 2 переменными
    n: величина Prognose Cumulative за прошлый год.
    k: полная выроботка энергии в предыдущем году
    """
    data0 = x[0]
    n = x[1]
    k = x[2]
    return data0 + (M * k) * (np.exp(-np.exp(B - C * n)))

def squareMistakeGompertz2(k: tuple, sales, total) -> float:
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
            z = sales[0], i, total[i-1]
            p = Gompertz2(z, k[0], k[1], k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res

import numpy as np

def Gompertz3(x, B, C, M) -> float:
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

