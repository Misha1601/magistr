# import json
import sys
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from matplotlib import pyplot

# определяем DataFrame Мировой
data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                     'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]})

# определяем DataFrame Европа
data1 = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                     'generate': [3.86302920121212, 4.82858524525252, 7.29549295555556, 11.1764791351515, 14.2443217667677, 22.4547142028283, 26.9342866553535, 36.4259493147475, 44.5311522856566, 59.296786859596, 71.0967493651913, 83.1641398783648, 105.713193767021, 121.353901497536, 135.383228613187, 153.443496864175, 186.657403230905, 215.032405064032, 248.115255753321, 264.815019959907, 318.931230019458, 322.867876348302, 384.216521406329, 403.217594774174, 460.029812809329, 510.138071007773]})

data_list = [data, data1]
metod_list = ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'trust-constr', 'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov']
sqrt_list = []

for k in data_list:
    data = k
    for n in metod_list:
        data['cum_sum'] = data['generate'].cumsum()
        data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]

        finalYear = 2025  # Финальный год

        def Bass(x, P, Q, M):
            """
            Функция расчета Prognose Sales
            x: величина Prognose Cumulative за прошлый год.
            """
            return (P*M+(Q-P)*(x))-(Q/M)*(x**2)

        # Начальные значения параметров
        # bounds = ([0, 0, 0], [np.inf, np.inf, np.inf])
        popt, pcov = curve_fit(Bass, data.generate, data.Sales, bounds=(0, np.inf), method='trf', maxfev = 10000)
        p0 = popt[0]
        q0 = popt[1]
        m0 = popt[2]
        # p0 = 0.0000012
        # q0 = 0.318
        # m0 = 12

        # print(f'Метод {n}')

        # Выводим стартовые коэффициенты
        # print('Стартовые коэффициенты:')
        # print(f'P0 = {p0}, Q0 = {q0}, M0 = {m0}')
        # print('Q0 =', q0)
        # print('M0 =', m0)

        def squareMistake(k: tuple, *sales) -> float:
            """
            Функция для минимизации через scipy.
            Рассчитывает сумму квадратов разностей значений
            Prognose Cumulative и Prognose Sales.
            k: кортеж начальных параметров (P, Q, M);
            sales: кортеж Sales.
            """
            # Начальные значения для первого года
            p0 = 0  # Prognose Sales
            c0 = sales[0]  # Prognose Cumulative
            res = 0  # Значение функции
            # Набираем результат функции за годы
            for i in range(1, len(sales)):
                p = Bass(c0, P=k[0], Q=k[1], M=k[2])  # Новый Prognose Sales
                c = c0 + p  # Новый Prognose Cumulative
                res += (c - sales[i])**2  # Добавляем
                # Обновляем значения
                p0 = p
                c0 = c
            return res


        # Формируем данные по годам
        years1 = tuple(data.year)
        gens = tuple(data.generate)

        # Готовим данные для минимизации
        k0 = [p0, q0, m0]  # Начальные значения параметров
        kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

        # Минимизируем сумму квадратов
        try:
            res = minimize(squareMistake, k0, args=gens, method=n, bounds=kb)
        except:
            # print(f'Метод {n} выдал ошибку')
            # sqrt_list.append(f'{n} - ошибка')
            continue
        print(res.success)

        # При неудачной минимизации сообщаем и выходим
        if not res.success:
            # print('Не удалось минимизировать функцию.')
            # sys.exit()
            continue

        k = tuple(res.x)  # Получаем кортеж параметров (P, Q, M)

        # Готовим данные для расчета прогнозов
        years2 = [years1[0]]  # Задаем начальный год
        prSales = [0]  # Задаем начальный Prognose Sales
        prCumul = [gens[0]]  # Задаем начальный Prognose Cumulative

        # Рассчитываем для всех лет
        while years2[-1] < finalYear:
            years2.append(years2[-1]+1)  # Год
            prSales.append(Bass(prCumul[-1], P=k[0], Q=k[1], M=k[2]))  # Prognose Sales
            prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative

        # Выводим коэффициенты
        # print('Коэффициенты:')
        # print(f' P = {k[0]},  Q = {k[1]},  M = {k[2]}')
        # print('Q =', k[1])
        # print('M =', k[2])

        # Выводим графики для контроля
        # pyplot.plot(years1, gens, label='Sales fact')  # Исходный
        pyplot.plot(years2, prCumul, label=f'Sales Bass, метод {n}')  # Расчитанный
        # pyplot.xlabel('year')  # Заголовок оси Х
        # pyplot.ylabel('generate')  # Заголовок оси Y
        # pyplot.legend()  # Отображаем имена данных
        # pyplot.show()  # Отображаем график

        # метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
        def rss(y_real, y_predicted):
            """Метрика суммы квадратов остатков, Результат должен быть наименьшим.
            """
            squared_residuals = np.square(np.subtract(y_real, y_predicted))
            return sum(squared_residuals)

        data['prCumul'] = prCumul[:len(gens)]
        y_real = data['generate']
        y_predicted = data['prCumul']
        # print(f"Сумма квадратов остатков - {rss(y_real, y_predicted)}")
        # print(data)
        sqrt_list.append(f'{n} {res.success} - {rss(y_real, y_predicted)}')

    print(sqrt_list)
    pyplot.plot(years1, gens, label='Sales fact')  # Исходный
    pyplot.xlabel('year')  # Заголовок оси Х
    pyplot.ylabel('generate')  # Заголовок оси Y
    pyplot.legend()  # Отображаем имена данных
    pyplot.show()  # Отображаем график