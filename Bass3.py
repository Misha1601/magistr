def Bass3(x, P, Q, K):
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
