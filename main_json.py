from Bass1 import Bass1, squareMistakeBass1
from Bass2 import Bass2, squareMistakeBass2
from Bass3 import Bass3, squareMistakeBass3
from Logic1 import Logic1, squareMistakeLogic1
from Logic2 import Logic2, squareMistakeLogic2
from Logic3 import Logic3, squareMistakeLogic3
from Gompertz1 import Gompertz1, squareMistakeGompertz1
from Gompertz2 import Gompertz2, squareMistakeGompertz2
from Gompertz3 import Gompertz3, squareMistakeGompertz3
from Functions import parser_json
from Functions import rss
from Functions import save_json
from Functions import linear_regression_extension
from Functions import log_error

# import json
# import os
# import shutil
# import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
import time
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def main(model_func):
    # распарсили json
    data, finalYear = parser_json()
    # print(data, finalYear)

    result = {}
    sqrt_list = []

    # Сохраняем в переменную все методы минимизации
    metod_list = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']

    # Поиск приближенных параметров
    try:
        match model_func.__name__:
            case 'Bass1':
                popt, pcov = curve_fit(Bass1, data.generate, data.Sales, bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Bass2':
                z = np.array([np.array(data.total[0:-1]), np.array(data.generate[1:])])
                popt, pcov = curve_fit(Bass2, z, np.array(data.Sales[1:]), bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Bass3':
                z = np.array([np.array(data.total[0:-1]), np.array(data.generate[1:]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Bass3, z, np.array(data.Sales[1:]), bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Logic1':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:])])
                popt, pcov = curve_fit(Logic1, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Logic2':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1])])
                popt, pcov = curve_fit(Logic2, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Logic3':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Logic3, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Gompertz1':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:])])
                popt, pcov = curve_fit(Gompertz1, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Gompertz2':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1])])
                popt, pcov = curve_fit(Gompertz2, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
            case 'Gompertz3':
                z = np.array([np.array(data.data0[1:]), np.array(data.index.values[1:]), np.array(data.total[0:-1]), np.array(data.costs[0:-1])])
                popt, pcov = curve_fit(Gompertz3, z, data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
                print(popt)
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
    for n in metod_list:
        # Минимизируем сумму квадратов
        match model_func.__name__:
            case 'Bass1':
                res = minimize(squareMistakeBass1, k0, args=np.array(data.generate), method=n, bounds=kb)
            case 'Bass2':
                res = minimize(squareMistakeBass2, k0, args=(np.array(data.generate), np.array(data.total)), method=n, bounds=kb)
            case 'Bass3':
                res = minimize(squareMistakeBass3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=n, bounds=kb)
            case 'Logic1':
                res = minimize(squareMistakeLogic1, k0, args=np.array(data.generate), method=n, bounds=kb)
            case 'Logic2':
                res = minimize(squareMistakeLogic2, k0, args=(np.array(data.generate), np.array(data.total)), method=n, bounds=kb)
            case 'Logic3':
                res = minimize(squareMistakeLogic3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=n, bounds=kb)
            case 'Gompertz1':
                res = minimize(squareMistakeGompertz1, k0, args=np.array(data.generate), method=n, bounds=kb)
            case 'Gompertz2':
                res = minimize(squareMistakeGompertz2, k0, args=(np.array(data.generate), np.array(data.total)), method=n, bounds=kb)
            case 'Gompertz3':
                res = minimize(squareMistakeGompertz3, k0, args=(np.array(data.generate), np.array(data.total), np.array(data.costs)), method=n, bounds=kb)

        k = tuple(res.x)  # Получаем кортеж параметров
        if not res.success:
            print(f'Метод {n} Не удалось минимизировать функцию!')
            print(f'{res.message}')
        # print(f'Метод {n} k = {k}')
        # определив параметры определяем данные для всех лет
        # Готовим данные для расчета прогнозов
        years2 = [data.year[0]]  # Задаем начальный год
        prSales = [0]  # Задаем начальный Prognose Sales
        prCumul = [data.generate[0]]  # Задаем начальный Prognose Cumulative

        ind_tgen = 1
        sum_prSales = data.generate[0]
        m = np.array(data.total)
        c = np.array(data.costs)
        # m = np.pad(m, (0, finalYear - data.year[0]), 'edge') # увеличивает массив последними значениями
        c = np.pad(c, (0, finalYear - data.year[0]), 'edge') # увеличивает массив последними значениями
        m = np.concatenate([m, linear_regression_extension(m, finalYear - tuple(data.year)[-1])]) # увеличивает массив регрессией
        # c += linear_regression_extension(c, finalYear - data.year[-1])  # при достижении 0 уходит в минус


        # Рассчитываем для всех лет
        while years2[-1] < finalYear:
            years2.append(years2[-1]+1)  # Год
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
            result[n] = {'years2':years2, 'prCumul':prCumul}
            y_predicted = prCumul[:len(data.generate)]
        else:
            result[n] = {'years2':years2, 'prCumul':prSales}
            y_predicted = prSales[:len(data.generate)]

        # метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
        sqrt_list.append([f'{n}', res.success, rss(data['generate'], y_predicted)])
        match model_func.__name__:
            case 'Bass1':
                square = squareMistakeBass1(k, data.generate)
            case 'Bass2':
                square = squareMistakeBass2(k, data.generate, data.total)
            case 'Bass3':
                square = squareMistakeBass3(k, data.generate, data.total, data.costs)
            case 'Logic1':
                square = squareMistakeLogic1(k, data.generate)
            case 'Logic2':
                square = squareMistakeLogic2(k, data.generate, data.total)
            case 'Logic3':
                square = squareMistakeLogic3(k, data.generate, data.total, data.costs)
            case 'Gompertz1':
                square = squareMistakeGompertz1(k, data.generate)
            case 'Gompertz2':
                square = squareMistakeGompertz2(k, data.generate, data.total)
            case 'Gompertz3':
                square = squareMistakeGompertz3(k, data.generate, data.total, data.costs)
        print(f'{k}, rss = {sqrt_list[-1][2]}, {n}, {square}')

    n = []
    for i in sqrt_list:
        if len(n) == 0:
            n = i
            continue
        if i[2] < n[2]:
            n = i

    print(f'Наменьшая сумма разницы квадратов у - {n[0]}, его rss = {n[2]}')
    data2 = dict(zip(result[n[0]]['years2'], result[n[0]]['prCumul']))

    # Сохраняем все в новый json аналогичный оригинальному но с обновленными данными
    save_json(data2)


if __name__ == '__main__':
    start_time = time.time()
    main(Bass1)
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} seconds')