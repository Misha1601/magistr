import json
import os
import shutil
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import time
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Получаем имя текущей директории и наличие файла Prognose_Request.json
current_dir = os.getcwd()
directory = str(current_dir)
files = os.listdir(directory)
doc = list(filter(lambda x: x[-5:] == '.json', files))

if 'Prognose_Request.json' not in doc:
    print('no file')

js_file = [os.path.join(current_dir, 'Prognose_Request.json')]

# Считываем  JSON file
with open(js_file[0]) as json_file:
    data_json = json.load(json_file)

# сохраняем в переменные, без нулевых показателей и с переводом значений в float
year = tuple(i['date'] for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
generate = tuple(float(i['fields'][0]['value'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
total = tuple(float(i['fields'][0]['total'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['total']) != 0)
costs = tuple(float(i['fields'][0]['costs'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['costs']) != 0)

# Создаем DataFrame из полученных данных
data = pd.DataFrame({'year': year, 'generate': generate, 'total': total, 'costs': costs})
data['cum_sum'] = data['generate'].cumsum()
data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]

# Считываем финальный год
finalYear = data_json['dataset']['end']

# for i in doc:
#     os.remove(os.path.join(current_dir, i))

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
        res = res + (c - sales[i])**2  # Добавляем
    return res

def rss(y_real, y_predicted):
    """Метрика суммы квадратов остатков, Результат должен быть наименьшим."""
    squared_residuals = np.square(np.subtract(y_real, y_predicted))
    return sum(squared_residuals)

def copy_and_rename_json_file(original_file_path, new_file_name):
    """Копируем и переименовывает оригинальный json файл"""
    # Извлечение имени файла из начального пути к нему
    original_file_name = os.path.basename(original_file_path)
    # Путь к новому файлу
    new_file_path = os.path.join(os.path.dirname(original_file_path), new_file_name)
    # Копирование файла и сохранение с новым именем
    shutil.copy(original_file_path, new_file_path)
    # Возвращение нового имени файла
    return new_file_name

def main():
    # Сохраняем в переменную все методы минимизации
    metod_list = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']
    vyvod = []
    signal = True
    r = 0
    ind = 0
    sqrt_list = []
    result = {}

    # Начальные значения параметров
    total_values = np.array(data.total[0:-1])
    generate_values = np.array(data.generate[1:])
    costs_values = np.array(data.costs[0:-1])
    Sales_values = np.array(data.Sales[1:])

    z = np.array([total_values, generate_values])
    popt, pcov = curve_fit(Bass2, z, Sales_values, bounds=(0, np.inf), method='trf', maxfev = 10000)

    p0 = popt[0]
    q0 = popt[1]
    m0 = popt[2]
    # print(z)
    print(f'p0 = {p0}')
    print(f'q0 = {q0}')
    print(f'm0 = {m0}')
    # Готовим данные для минимизации
    k0 = [p0, q0, m0]  # Начальные значения параметров
    kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

    generate2 = np.array(data.generate)
    total2 = np.array(data.total)

    for n in metod_list:
        # Минимизируем сумму квадратов
        try:
            res = minimize(squareMistakeBass2, k0, args=(generate2, total2), method=n, bounds=kb)
        except:
            print(f'Для {n} - не минимизировалось')
            continue

        k = tuple(res.x)  # Получаем кортеж параметров (P, Q, M)

        if not res.success:
            print(f'Метод {n} Не удалось минимизировать функцию!')
        # print(f'Метод {n} k = {k}')

        # Готовим данные для расчета прогнозов
        years2 = [year[0]]  # Задаем начальный год
        prSales = [0]  # Задаем начальный Prognose Sales
        prCumul = [generate[0]]  # Задаем начальный Prognose Cumulative

        ind_tgen = 1
        sum_prSales = generate[0]
        m = np.array(data.total)
        c = np.array(data.costs)
        m = np.pad(m, (0, finalYear - year[0]), 'edge')
        c = np.pad(c, (0, finalYear - year[0]), 'edge')


        # Рассчитываем для всех лет
        while years2[-1] < finalYear:
            years2.append(years2[-1]+1)  # Год
            z = m[ind_tgen - 1], sum_prSales
            bs = Bass2(z, k[0], k[1], k[2])
            prSales.append(bs)  # Prognose Sales
            prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative
            sum_prSales += bs
            ind_tgen += 1

        result[n] = {'years2':years2, 'prCumul':prCumul}

        # метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
        data['prCumul'] = prCumul[:len(generate)]
        y_real = data['generate']
        y_predicted = data['prCumul']
        sqrt_list.append([f'{n}', res.success, rss(y_real, y_predicted)])
        square = squareMistakeBass2(k, generate, total)
        print(f'{k}, rss = {sqrt_list[-1][2]}, {n}, {square}')

    n = []
    for i in sqrt_list:
        if len(n) == 0:
            n = i
            continue
        if i[2] < n[2]:
            n = i

    print(f'Наменьшая сумма разницы квадратов у - {n[0]}')
    data2 = dict(zip(result[n[0]]['years2'], result[n[0]]['prCumul']))

    # # Write the JSON file
    file_name = 'dataOut.json'
    copy_and_rename_json_file(js_file[0], file_name)

    for key, value in data2.items():
            for i in data_json['dataset']['records']:
                if i['date'] == key:
                    i['fields'][0]['value'] = str(value)
                    break
            else:
                data_json['dataset']['records'].append({'date':key, 'fields':[{'name': "Generation wind world", "datatype": "double", 'value':str(value)}]})

    with open('dataOut.json', 'w') as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} seconds')