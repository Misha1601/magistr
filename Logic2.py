import numpy as np

def Logic2(x, B, C, M):
    """
    Функция расчета Prognose Sales с 2 переменными
    n: величина Prognose Cumulative за прошлый год.
    k: полная выроботка энергии в предыдущем году
    """
    data0 = x[0]
    n = x[1]
    k = x[2]
    return data0 + (M * k) * (1/(1+np.exp(-B * (n - C))))

def squareMistakeLogic2(k: tuple, sales, total1) -> float:
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
            z = sales[0], i, total1[i-1]
            p = Logic2(z, k[0], k[1], k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res
