from pprint import pprint
from matplotlib import pyplot
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

from Functions import linear_regression_extension


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

def execute_sql_query(sql_query):
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
        cursor.execute(sql_query)
        # Получение результатов запроса
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
    Возвращает список значений диффузии, год и параметры.
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
        log_error('error_curve_fit.txt', f'Для {model_func.__name__}, данные содержат NaN или используются несовместимые параметры!')
        return None
    except RuntimeError:
        log_error('error_curve_fit.txt', f'Для {model_func.__name__}, минимизация по методу наименьших квадратов не удалась!')
        return None
    except OptimizeWarning:
        log_error('error_curve_fit.txt', f'Для {model_func.__name__}, ковариацию параметров невозможно оценить!')
        return None
    # Создаем цикл и выполняем минимизацию для каждого из методов
    k0 = [popt[0], popt[1], popt[2]]  # Начальные значения параметров
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
    if not res.success:
        return None

    # определив начальные параметры определяем данные для всех лет
    # Готовим данные для расчета прогнозов
    years0 = [data.year[0]]  # Задаем начальный год
    prSales = [0]  # Задаем начальный Prognose Sales
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
        return prCumul, years0, k
    else:
        return prSales, years0, k

def func_minus_year(data, numberP, numberS, model, metod, country):
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
    pyplot.plot(data.year, data.generate, label='Sales fact', color='black', linewidth=1, zorder=3)  # Исходный график
    # на сколько лет вперед предсказываем
    # numberP = 5
    # какой шаг используем по годам
    numberStep = numberS
    finalYear = list(data.year)[-1] + numberP
    # print(data)
    result = func_dif_innov(data, finalYear, model, metod)
    results = {}
    results[f'result{finalYear}'] = result[0]
    pyplot.plot(result[1], result[0], label=f'result{finalYear}')
    while True:
        data1 = data[:-numberStep]
        print(list(data1.year)[-1])
        finalYear = list(data1.year)[-1] + numberP
        # print(list(data1.year)[-1], finalYear)
        result = func_dif_innov(data1, finalYear, model, metod)
        if result:
            results[f'result{finalYear}'] = result[0]
            pyplot.plot(result[1], result[0], label=f'result{finalYear}')
        else:
            break
        numberStep += numberS
        print(numberStep)
    # print(results)

    pyplot.title(f'Данные для {country}, модель {model.__name__}, шаг измерения - {numberS}, предсказывает на {numberP} лет')
    pyplot.legend()  # Отображаем имена данных
    pyplot.show()  # Отображаем график

if __name__ == '__main__':
    start_time2 = time.time()
    data_generate_test = {'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193],
    'total':[13375.2439634053, 13789.2495277064, 14120.5171345097, 14502.9192434368, 14917.7637553936, 15555.5482906317, 15788.8606107222, 16345.4843195876, 16924.0184060025, 17726.7475122076, 18454.1188104507, 19155.2911176488, 20045.9829957051, 20421.6373537822, 20264.8910596484, 21570.6888619834, 22256.9952443638, 22806.2764799403, 23435.2382123808, 24031.7070496167, 24270.5009409496, 24915.1871081891, 25623.8922507836, 26659.1362380925, 27000.9508509267, 26823.2483500223],
    'costs':[0.196, 0.178, 0.157, 0.139, 0.134, 0.142, 0.126, 0.119, 0.106, 0.111, 0.104, 0.105, 0.098, 0.088, 0.087, 0.086, 0.083, 0.083, 0.082, 0.076, 0.069, 0.066, 0.064, 0.058, 0.053, 0.05]}

    select_all_region = f'SELECT DISTINCT "Region" FROM Wind'
    # print(select_all_region)
    data_all_region = [column[0] for column in execute_sql_query(select_all_region)]
    # print(data_all_region)

    select_all_country = f'SELECT DISTINCT "Country" FROM Wind'
    # print(select_all_country)
    data_all_country = [column[0] for column in execute_sql_query(select_all_country)]
    # print(data_all_country)

    select_year = f"PRAGMA table_info(Wind)"
    data_year = [column[1] for column in execute_sql_query(select_year)]
    # print(data_year)

    select_total = f'SELECT * FROM Wind WHERE Country="Total"'
    # print(select_total)
    data_total = execute_sql_query(select_total)[0]
    # print(data_total)

    select_costs = f'SELECT * FROM Wind WHERE Country="Costs"'
    # print(select_costs)
    data_costs = execute_sql_query(select_costs)[0]
    # print(data_costs[2:])

    country  = 'China'
    # country  = 'Total World'
    select_country = f'SELECT * FROM Wind WHERE Country="{country}"'
    # print(select_country)
    data_country = execute_sql_query(select_country)[0]
    # print(data_country)

    finalYear = 2025
    models = [Bass1, Bass2, Bass3, Logic1, Logic2, Logic3, Gompertz1, Gompertz2, Gompertz3]
    metods = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']

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




    # for i in models:
    #     result = func_dif_innov(data, finalYear, i, metods[0])
    #     print(f'Модель {i.__name__} - {result[2]}')
        # for i in result:
        #     print(i)

    func_minus_year(data, 5, 2, models[0], metods[0], country)


    end_time2 = time.time()
    total_time2 = end_time2 - start_time2
    print(f'Общее время выполнения: {total_time2} seconds')
