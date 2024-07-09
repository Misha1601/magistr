def Bass1(x, P, Q, M):
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
