def Bass2(x, P, Q, K):
    """
    Функция расчета Prognose Sales с 2 переменными
    y = Y(t-1) сумма предыдущих прогнозов, где y0 первое фактическое сгенерированное
    m = М(t-1) общая генерация электроэнергии в предыдущий период за год
        """
    m = x[0]
    y = x[1]
    return (P * m * K + (Q - P) * y - (Q / (m * K) * y ** 2))

def squareMistakeBass2(k: tuple, sales, total1) -> float:
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
        z = total1[i-1], c
        p = Bass2(z, k[0], k[1], k[2])  # Новый Prognose Sales
        c = c + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем
    return res
