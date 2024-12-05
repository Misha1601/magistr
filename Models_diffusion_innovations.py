from pprint import pprint
from matplotlib import pyplot
import json
import pandas as pd
import numpy as np
import sqlite3
import time
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


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

def linear_regression_extension(original_array, n):
    """
    Продолжает массив на n элементов используя линейную аппроксимацию.
    Parameters:
    - original_array: Исходный массив
    - n: Количество новых элементов
    Returns:
    - Массив предсказанных значений
    """
    x = np.arange(len(original_array))
    coeffs = np.polyfit(x, original_array, 1)  # 1 - степень полинома (линейная)
    new_x = np.arange(len(original_array), len(original_array) + n)
    return np.polyval(coeffs, new_x)

def execute_sql_query(sql_query, params=None):
    """
    Выполняет SQL-запрос к базе данных SQLite и возвращает результат в виде pd.DataFrame.
    :param sql_query: SQL-запрос для выполнения.
    :return: Список с результатами запроса.
    """
    try:
        # Подключение к базе данных SQLite
        conn = sqlite3.connect('Wind.db')
        cursor = conn.cursor()
        # Выполнение SQL-запроса
        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)

        # Проверка типа запроса
        if any(keyword in sql_query.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE']):
            # Если это запрос на изменение данных, сохраняем изменения
            conn.commit()
            conn.close()
        else:
            # Если это запрос на выборку данных, получаем результаты
            results = cursor.fetchall()
            # Закрытие соединения с базой данных
            conn.close()
            return results
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

def func_dif_innov(data, finalYear: int, model_func, metod: str):
    """Функция диффузии иновации.
    Принимает
    data - готовый pd.DataFrame
    finalYear - конечный год для предсказания, формат int,
    model_func - модель диффузии,
    metod = один из методов минимизации, формат str,
    Возвращает список значений диффузии, список лет, параметры.
    """

    # Поиск приближенных параметров
    try:
        match model_func.__name__:
            case 'Bass1':
                popt, pcov = curve_fit(Bass1, data.generate, data.Sales, bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Bass2':
                z = np.array([np.array(data.total[0:-1]), np.array(data.generate[1:])])
                popt, pcov = curve_fit(Bass2, z, np.array(data.Sales[1:]), bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Bass3':
                z = np.array([np.array(data.total[0:-1]), np.array(data.generate[1:]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Bass3, z, np.array(data.Sales[1:]), bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Logic1':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:])])
                popt, pcov = curve_fit(Logic1, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Logic2':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1])])
                popt, pcov = curve_fit(Logic2, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Logic3':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Logic3, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Gompertz1':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:])])
                popt, pcov = curve_fit(Gompertz1, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Gompertz2':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1])])
                popt, pcov = curve_fit(Gompertz2, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
            case 'Gompertz3':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Gompertz3, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
    except ValueError:
        print(f'Для {model_func.__name__}, данные содержат NaN или используются несовместимые параметры!')
        return None
    except RuntimeError:
        print(f'Для {model_func.__name__}, минимизация по методу наименьших квадратов не удалась!')
        return None
    except OptimizeWarning:
        print(f'Для {model_func.__name__}, ковариацию параметров невозможно оценить!')
        return None
    # Создаем цикл и выполняем минимизацию для каждого из методов
    k0 = (popt[0], popt[1], popt[2])  # Начальные значения параметров
    kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные


    # total_time = time.time() - end_time
    # print(f'Время между приближёнными и минимизацией: {total_time} seconds')
    # end_time = time.time()


    # Минимизируем сумму квадратов
    match model_func.__name__:
        case 'Bass1':
            res = minimize(squareMistakeBass1, k0, args=np.array(data.generate), method=metod, bounds=kb)
        case 'Bass2':
            res = minimize(squareMistakeBass2, k0, args=(np.array(data.generate), np.array(data.total)), method=metod, bounds=kb)
        case 'Bass3':
            res = minimize(squareMistakeBass3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=metod, bounds=kb)
        case 'Logic1':
            res = minimize(squareMistakeLogic1, k0, args=np.array(data.generate), method=metod, bounds=kb)
        case 'Logic2':
            res = minimize(squareMistakeLogic2, k0, args=(np.array(data.generate), np.array(data.total)), method=metod, bounds=kb)
        case 'Logic3':
            res = minimize(squareMistakeLogic3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=metod, bounds=kb)
        case 'Gompertz1':
            res = minimize(squareMistakeGompertz1, k0, args=np.array(data.generate), method=metod, bounds=kb)
        case 'Gompertz2':
            res = minimize(squareMistakeGompertz2, k0, args=(np.array(data.generate), np.array(data.total)), method=metod, bounds=kb)
        case 'Gompertz3':
            res = minimize(squareMistakeGompertz3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=metod, bounds=kb)

    k = tuple(res.x)  # Получаем кортеж параметров
    # if not res.success:
    #     return None

    # определив начальные параметры определяем данные для всех лет
    # Готовим данные для расчета прогнозов
    years0 = [data.year[0]]  # Задаем начальный год
    prSales = [data.generate[0]]  # Задаем начальный Prognose Sales
    prCumul = [data.generate[0]]  # Задаем начальный Prognose Cumulative
    ind_tgen = 1
    sum_prSales = data.generate[0]
    m = np.array(data.total)
    c = np.array(data.costs)
    c = np.pad(c, (0, finalYear - data.year[0]), 'edge') # увеличивает массив последними значениями
    m = np.concatenate([m, linear_regression_extension(m, finalYear - tuple(data.year)[-1])]) # увеличивает массив регрессией

    # Рассчитываем для всех лет
    while years0[-1] < finalYear:
        years0.append(years0[-1]+1)  # Год
        # Prognose Sales
        match model_func.__name__:
            case 'Bass1':
                prSales.append(Bass1(prCumul[-1], k[0], k[1], k[2]))  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
            case 'Bass2':
                z = m[ind_tgen - 1], sum_prSales
                bs = Bass2(z, k[0], k[1], k[2])
                prSales.append(bs)  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
                sum_prSales += bs
                ind_tgen += 1
            case 'Bass3':
                z = m[ind_tgen - 1], sum_prSales, c[ind_tgen - 1]
                bs = Bass3(z, k[0], k[1], k[2])
                prSales.append(bs)  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
                sum_prSales += bs
                ind_tgen += 1
            case 'Logic1':
                prSales.append(Logic1((data.generate[0], ind_tgen), k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Logic2':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1]  # indexdata, total_values
                prSales.append(Logic2(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Logic3':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1], c[ind_tgen - 1]   # indexdata, total_values
                prSales.append(Logic3(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz1':
                prSales.append(Gompertz1((data.generate[0], ind_tgen), k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz2':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1]  # indexdata, total_values
                prSales.append(Gompertz2(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz3':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1], c[ind_tgen - 1]   # indexdata, total_values
                prSales.append(Gompertz3(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер

    if model_func.__name__ in ['Bass1', 'Bass2', 'Bass3']:
        return prCumul, years0, k, k0
    else:
        return prSales, years0, k, k0

def func_dif_innov_0_parametr(data, p0, p1, p2, model_func, metod: str):
    """Функция диффузии иновации c 0 параметрами без предсказания.
    Принимает
    data - готовый pd.DataFrame
    model_func - модель диффузии,
    metod = один из методов минимизации, формат str,
    Возвращает список значений диффузии, список лет, параметры.
    """

    k = p0, p1, p2  # Получаем кортеж параметров

    # определив начальные параметры определяем данные для всех лет
    # Готовим данные для расчета прогнозов
    years0 = [data.year[0]]  # Задаем начальный год
    finalYear = list(data.year)[-1]  # Задаем Конечный год
    prSales = [data.generate[0]]  # Задаем начальный Prognose Sales
    prCumul = [data.generate[0]]  # Задаем начальный Prognose Cumulative
    # print(prCumul)
    ind_tgen = 1
    sum_prSales = data.generate[0]
    # print(sum_prSales)
    m = np.array(data.total)
    c = np.array(data.costs)

    # Рассчитываем для всех лет
    while years0[-1] < finalYear:
        years0.append(years0[-1]+1)  # Год
        # Prognose Sales
        match model_func.__name__:
            case 'Bass1':
                prSales.append(Bass1(prCumul[-1], k[0], k[1], k[2]))  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
            case 'Bass2':
                z = m[ind_tgen - 1], sum_prSales
                bs = Bass2(z, k[0], k[1], k[2])
                prSales.append(bs)  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
                sum_prSales += bs
                ind_tgen += 1
            case 'Bass3':
                z = m[ind_tgen - 1], sum_prSales, c[ind_tgen - 1]
                bs = Bass3(z, k[0], k[1], k[2])
                prSales.append(bs)  # Prognose Sales
                prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
                sum_prSales += bs
                ind_tgen += 1
            case 'Logic1':
                prSales.append(Logic1((data.generate[0], ind_tgen), k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Logic2':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1]  # indexdata, total_values
                prSales.append(Logic2(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Logic3':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1], c[ind_tgen - 1]   # indexdata, total_values
                prSales.append(Logic3(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz1':
                prSales.append(Gompertz1((data.generate[0], ind_tgen), k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz2':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1]  # indexdata, total_values
                prSales.append(Gompertz2(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер
            case 'Gompertz3':
                z = data.generate[0], ind_tgen, m[ind_tgen - 1], c[ind_tgen - 1]   # indexdata, total_values
                prSales.append(Gompertz3(z, k[0], k[1], k[2]))  # Добавляем следующий Prognose
                ind_tgen += 1  # Увеличиваем порядковый номер

    if model_func.__name__ in ['Bass1', 'Bass2', 'Bass3']:
        return prCumul, years0
    else:
        return prSales, years0

def func_minus_year(country, numberP, numberS, model, metod):
    """Функция func_minus_year используется для построения графика продаж данных для конкретной страны и модели за определенное количество лет.
    Данные выводятся для исходного количества лет, а затем функция прогнозирует продажи на дополнительные годы с шагом, указанным пользователем.
    Прогнозируемые данные затем выводятся на том же графике.
    Параметры:
    data: (pandas DataFrame) Данные продаж для конкретной страны и модели.
    numberP: (int) Количество лет, на которое прогнозируется.
    numberS: (int) Шаг, по которому прогнозируются данные продаж.
    model: (str) Название модели, используемой для прогнозирования.
    metod: (str) Название метода, используемого для прогнозирования.
    country: (str) Название страны, для которой выводятся данные.
    Функция не возвращает значение. Она отображает график продаж данных и прогнозируемых данных на том же графике.
    """
    # проверяем что такие данные уже есть, если есть, выходим
    select_results = f'SELECT * FROM results WHERE Country="{country}" AND prognos="{numberP}" AND step="{numberS}" AND model="{model.__name__}"'
    # print(select_results)
    data_results = execute_sql_query(select_results)
    # print(data_results)
    if data_results:
        return None



    select_year = f"PRAGMA table_info(Wind)"
    data_year = [column[1] for column in execute_sql_query(select_year)]
    # print(data_year)

    select_total = f'SELECT * FROM Wind WHERE Country="Total {country}"'
    # print(select_total)
    data_total = execute_sql_query(select_total)[0]
    # print(data_total)

    select_costs = f'SELECT * FROM Wind WHERE Country="Costs"'
    # print(select_costs)
    data_costs = execute_sql_query(select_costs)[0]
    # print(data_costs[2:])

    country = country
    # country  = 'World'
    select_country = f'SELECT * FROM Wind WHERE Country="{country}"'
    # print(select_country)
    data_country = execute_sql_query(select_country)[0]
    # print(data_country)

    data_generate = {'year': [int(i) for i in data_year[2:]],
                     'generate': data_country[2:],
                     'total': data_total[2:],
                     'costs': data_costs[2:]}

    # определяем DataFrame
    data = pd.DataFrame(data_generate)
    # data = pd.DataFrame(data_generate_test) # для теста закоментировать два предыдущих, это раскоментировать
    data['cum_sum'] = data['generate'].cumsum()
    data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]
    data['data0'] = data['generate'][0]


    # подготовим информацию для вставки в БД
    columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0', 'year_test', 'data_origin', 'data_prognos', 'otclonenie', 'otclonenie_procent', 'MAE', 'MAE_pribl', 'MAE_procent']
    # columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0']
    line = [country, str(numberP), '-', model.__name__, metod]



    # pyplot.plot(data.year, data.generate, label='Sales fact', color='black', linewidth=1, zorder=3)  # Исходный график
        # шаг используемый по годам
    numberStep = numberS
    # данные с предсказанием на указанный год
    finalYear = list(data.year)[-1] + numberP
    # print(data)
    result1 = func_dif_innov(data, finalYear, model, metod)
    if result1 == None:
        return None
    line.append(result1[-2]) # param
    line.append(result1[-1]) # param0
    line.append(list(data['year'])[-1]) # year_test
    line.append('-') # data_origin
    line.append(float(result1[0][-1])) # data_prognos
    line.append('-') # otclonenie
    line.append('-') # otclonenie_procent
    line.append('-') # MAE Средняя абсолютная ошибка (MAE)
    line.append('-') # MAE_pribl Средняя абсолютная ошибка (MAE)
    line.append('-') # MAE_procent Разница в % между крайними значениями MAE
    columns += result1[1] # Добавляем полученные года
    line += result1[0] # Результат по каждому году
    columns_str = ', '.join(f"'{col}'" for col in columns)
    placeholders = ', '.join(f"'{i}'" for i in line)
    insert1 = f'INSERT INTO results ({columns_str}) VALUES ({placeholders})'
    execute_sql_query(insert1)

    # добаляем данные без предсказания
    # проверяем что такие данные уже есть, если есть не добавляем
    select_results0 = f'SELECT * FROM results WHERE Country="{country}" AND prognos="0" AND step="0" AND model="{model.__name__}"'
    # print(select_results0)
    data_results0 = execute_sql_query(select_results0)
    # print(data_results0)
    if not data_results0:
        p0, p1, p2 = result1[-2]
        # print(p0, p1, p2)
        result0 = func_dif_innov_0_parametr(data, p0, p1, p2, model, metod)
        # подготовим информацию для вставки в БД
        # columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0']
        columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0', 'year_test', 'data_origin', 'data_prognos', 'otclonenie', 'otclonenie_procent', 'MAE', 'MAE_pribl', 'MAE_procent']
        line = [country, '0', '0', model.__name__, metod, '-', result1[-1]]
        line.append('-') # year_test
        line.append(float(list(data['generate'])[-1])) # data_origin
        line.append(float(result0[0][-1])) # data_prognos
        line.append(float(list(data['generate'])[-1])-float(result0[0][-1])) # otclonenie
        if float(list(data['generate'])[-1]) == 0:
            line.append(0) # otclonenie_procent
        else:
            line.append(np.abs((float(list(data['generate'])[-1])-float(result0[0][-1]))/float(list(data['generate'])[-1])*100)) # otclonenie_procent
        mae = np.mean(np.abs(np.array(list(data['generate'])) - np.array(result0[0])))
        line.append(mae) # MAE Средняя абсолютная ошибка (MAE)
        line.append('-') # MAE_pribl Средняя абсолютная ошибка (MAE)
        line.append('-') # MAE_procent Разница в % между крайними значениями MAE
        columns += result0[1] # Добавляем полученные года
        line += result0[0] # Результат по каждому году
        columns_str = ', '.join(f"'{col}'" for col in columns)
        placeholders = ', '.join(f"'{i}'" for i in line)
        insert0 = f'INSERT INTO results ({columns_str}) VALUES ({placeholders})'
        # print(insert0)
        execute_sql_query(insert0)
    else:
        # Извлечение данных
        conn = sqlite3.connect('Wind.db')
        result0 = pd.read_sql_query(select_results0, conn)
        conn.close()
        # Фильтруем столбцы, которые являются годами
        filtered_columns = [col for col in result0.columns if col.isdigit() and len(col) == 4]
        result0 = result0[filtered_columns].astype(float)
        result0 = [[i for i in result0.values[0] if not np.isnan(i)]]

    # если шаг = 0 или прогноз слишком большой, выходим из программы
    if int(numberS) == 0:
        return None

    if int(numberP) >= 6:
        numberStep = 5
        numberP1 = 5
        numberS1 = 5
        # проверяем что такие данные уже есть, если есть, выходим
        select_results = f'SELECT * FROM results WHERE Country="{country}" AND prognos="{numberP1}" AND step="{numberS1}" AND model="{model.__name__}"'
        # print(select_results)
        data_results = execute_sql_query(select_results)
        # print(data_results)
        if data_results:
            return None
    else:
        numberStep = numberS
        numberP1 = numberP
        numberS1 = numberS

    while True:
        # columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0']
        columns = ['country', 'prognos', 'step', 'model', 'metod', 'param', 'param0', 'year_test', 'data_origin', 'data_prognos', 'otclonenie', 'otclonenie_procent', 'MAE', 'MAE_pribl', 'MAE_procent']
        line = [country, numberP1, numberS1, model.__name__, metod]
        data1 = data[:-numberStep]
        if list(data1.year)[-1] <= 2001:
            break
        # print(list(data1.year)[-1])
        finalYear = list(data1.year)[-1] + numberP1
        # print(list(data1.year)[-1], finalYear)
        result2 = func_dif_innov(data1, finalYear, model, metod)
        if result2:
            line.append(result2[-2]) # param
            line.append(result2[-1]) # param0

            line.append(list(data1.year)[-1]) # year_test
            ind = numberStep - numberS1
            if ind == 0:
                res_gen = float(list(data['generate'])[-1])
                res_gen_list = list(data['generate'])
                res_gen_pribl = result0[0]
            else:
                res_gen = float(list(data[:-ind]['generate'])[-1])
                res_gen_list = list(data[:-ind]['generate'])
                res_gen_pribl = result0[0][:-ind]
            line.append(res_gen) # data_origin
            line.append(float(result2[0][-1])) # data_prognos
            line.append(res_gen-float(result2[0][-1])) # otclonenie
            if res_gen == 0:
                line.append(0) # otclonenie_procent
            else:
                line.append(np.abs((res_gen-float(result2[0][-1]))/res_gen*100)) # otclonenie_procent
            mae = np.mean(np.abs(np.array(res_gen_list) - np.array(result2[0])))
            line.append(mae) # MAE Средняя абсолютная ошибка (MAE)
            mae2 = np.mean(np.abs(np.array(res_gen_pribl) - np.array(result2[0])))
            line.append(mae2) # MAE_pribl Средняя абсолютная ошибка (MAE)
            mae_pr = float(result0[0][:len(result2[0])][-1])
            if mae_pr == 0:
                line.append(0) # MAE_procent
            else:
                line.append(np.abs(mae_pr-float(result2[0][-1]))/mae_pr*100) # MAE_procent Разница в % между крайними значениями MAE
            columns += result2[1]
            line += result2[0]
            columns_str = ', '.join(f"'{col}'" for col in columns)
            placeholders = ', '.join(f"'{i}'" for i in line)
            insert2 = f'INSERT INTO results ({columns_str}) VALUES ({placeholders})'
            execute_sql_query(insert2)

            # pyplot.plot(result2[1], result2[0], label=f'result{finalYear}')
        else:
            break
        numberStep += numberS1
        # print(numberStep)
    # pprint(results)

    # pyplot.title(f'Данные для {country}, модель {model.__name__}, шаг измерения - {numberS}, предсказывает на {numberP} лет')
    # pyplot.legend()  # Отображаем имена данных
    # pyplot.show()  # Отображаем график

def analyze_data(country, prognos, step, model, metod):
    """Функция для анализа данных"""
    # Извлечение данных
    conn = sqlite3.connect('Wind.db')
    query = f"SELECT * FROM Wind WHERE Country = ?"
    wind_data = pd.read_sql_query(query, conn, params=[country])
    query_p = f"SELECT * FROM results WHERE country = ? AND prognos = ? AND step = ? AND model = ? AND metod = ?"
    results_data = pd.read_sql_query(query_p, conn, params=[country, prognos, step, model, metod])
    conn.close()

    # Фильтруем столбцы, которые являются годами
    filtered_columns_wind = [col for col in wind_data.columns if col.isdigit() and len(col) == 4]

    # Обрезаем DataFrame до столбцов, которые являются годами
    # Оригинальные данные до предсказания
    original_data_wind = wind_data[filtered_columns_wind].astype(float)
    original_year = [int(i) for i in filtered_columns_wind]
    original_values = [i for i in original_data_wind.values[0]]
    len_original_values = len(original_values)
    result_dict = {}
    result_dict[country] = {}
    result_dict[country][prognos] = {}
    result_dict[country][prognos][step] = {}
    result_dict[country][prognos][step][model] = {}
    result_dict[country][prognos][step][model][metod] = {}
    result_dict[country][prognos][step][model][metod]['origen'] = original_year, original_values

    # Анализ данных
    for index, row in results_data.iterrows():
        year_end = int(row.last_valid_index())
        year_start = year_end - prognos

        # Создаем новый DataFrame из строки
        new_df = row.to_frame().T

        if year_end > int(filtered_columns_wind[-1]):
            # print(year_end)
            predicted_data = new_df[filtered_columns_wind].astype(float)
            year_full = [col for col in new_df.columns if col.isdigit() and len(col) == 4 and int(col)<=int(row.last_valid_index())]
            year_full_int = [int(i) for i in year_full]
            predicted_values = [i for i in new_df[year_full].astype(float).values[0] if i != None]
            if len(original_values) >= len(predicted_values):
                # Среднеквадратичное отклонение (RMSE)
                rmse = np.sqrt(np.mean((np.array(original_values[:len(predicted_values)]) - np.array(predicted_values))**2))
                # Средняя абсолютная ошибка (MAE)
                mae = np.mean(np.abs(np.array(original_values[:len(predicted_values)]) - np.array(predicted_values)))
                # Метрика суммы квадратов остатков, Результат должен быть наименьшим.
                squared = np.square(np.subtract(original_values[:len(predicted_values)], predicted_values))
                # print(squared)
            else:
                # Среднеквадратичное отклонение (RMSE)
                # print(original_values)
                # print(predicted_values[:len(predicted_values)])
                rmse = np.sqrt(np.mean((np.array(original_values) - np.array(predicted_values[:len(original_values)]))**2))
                # Средняя абсолютная ошибка (MAE)
                mae = np.mean(np.abs(np.array(original_values) - np.array(predicted_values[:len(original_values)])))
                # Метрика суммы квадратов остатков, Результат должен быть наименьшим.
                squared = np.square(np.subtract(original_values, predicted_values[:len(original_values)]))
                # print(squared)
            result_dict[country][prognos][step][model][metod][year_full[-1]] = year_full_int, predicted_values, rmse, mae, sum(squared)
        else:
            predicted_data = new_df[filtered_columns_wind].astype(float)
            year_full = [col for col in new_df.columns if col.isdigit() and len(col) == 4 and int(col)<=int(row.last_valid_index())]
            year_full_int = [int(i) for i in year_full]
            predicted_values = [i for i in new_df[year_full].astype(float).values[0] if i != None]
            len_predicted_values = len(predicted_values)
            if len_original_values >= len_predicted_values:
                new_original_values = original_values[:len_predicted_values]
                new_predicted_values = predicted_values
            else:
                new_predicted_values = predicted_values[:len_original_values]
                new_original_values = original_values
            y_true = np.array(new_original_values)
            y_pred = np.array(new_predicted_values)

            # Среднеквадратичное отклонение (RMSE)
            rmse = np.sqrt(np.mean((y_true - y_pred)**2))
            # Средняя абсолютная ошибка (MAE)
            mae = np.mean(np.abs(y_true - y_pred))
            # Метрика суммы квадратов остатков, Результат должен быть наименьшим.
            squared = np.square(np.subtract(y_true, y_pred))
            result_dict[country][prognos][step][model][metod][year_full[-1]] = year_full_int, predicted_values, rmse, mae, sum(squared)
    return result_dict
if __name__ == '__main__':
    start_time2 = time.time()

    select_all_region = f'SELECT DISTINCT "Region" FROM Wind '
    data_all_region = [column[0] for column in execute_sql_query(select_all_region)]

    select_all_country = f'SELECT DISTINCT "Country" FROM Wind WHERE "Region" != "-" AND "Country" NOT LIKE "%Total%"'
    data_all_country = [column[0] for column in execute_sql_query(select_all_country)]
    # print(data_all_country)

    # finalYear = 2025
    models = [Bass1, Bass2, Bass3, Logic1, Logic2, Logic3, Gompertz1, Gompertz2, Gompertz3]
    metods = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']


    # execute_sql_query('DELETE FROM results;')
    z = 1
    # for i in data_all_country:
    #     for k in range(5, 0, -1):
    #         for l in models:
                # for m in metods:
                    # print(z, i, k, 5, l.__name__, metods[0])
                    # func_minus_year(i, k, 5, l, metods[0])
                    # z += 1
                    # pass
    # result_dict = {}
    # result_list = []
    # for i in data_all_country:
    #     for l in models:
    #         print(z, i, 5, 5, l.__name__, metods[0])
    #         my_dict = analyze_data(i, 5, 5, l.__name__, metods[0])
            # with open('result_dict.json', 'a') as json_file:
            #     json.dump(my_dict, json_file, indent=4)
            # for n in my_dict[i][5][5][l.__name__][metods[0]].keys():
            #     if n != 'origen':
            #         result_list1 = [i, 5, 5, l.__name__, metods[0], n, my_dict[i][5][5][l.__name__][metods[0]][n][2], my_dict[i][5][5][l.__name__][metods[0]][n][3], my_dict[i][5][5][l.__name__][metods[0]][n][4]]
            #         result_list.append(result_list1)
            # z += 1

    # Создаем DataFrame
    # df = pd.DataFrame(result_list, columns=['country','prog', 'step', 'model', 'metod', 'year', 'rmse', 'mae', 'sum'])
    # Записываем в Excel
    # df.to_excel('result_list.xlsx', index=False)

    # for i in result_list:
    #     print(i)



    # execute_sql_query('DELETE FROM results;')
    for i in models:
    #     for k in data_all_country:
    #         func_minus_year(k, 5, 5, i, metods[0])

        func_minus_year('Canada', 30, 5, i, metods[0])


    end_time2 = time.time()
    total_time2 = end_time2 - start_time2
    print(f'Общее время выполнения: {total_time2} seconds')
