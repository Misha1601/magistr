import numpy as np

def Gompertz1(x, B, C, M):
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
