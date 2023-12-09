import numpy as np

def Logic1(x, B, C, M):
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
