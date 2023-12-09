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


def main():
    # Получаем имя текущей директории
    current_dir = os.getcwd()
    directory = str(current_dir)
    files = os.listdir(directory)
    doc = list(filter(lambda x: x[-5:] == '.json', files))

    # if len(js_file) == 0:
    #     print('No file')
    #     return None

    if 'Prognose_Request.json' not in doc:
        print('no file')
        return None

    js_file = [os.path.join(current_dir, 'Prognose_Request.json')]

    # Open the JSON file
    with open(js_file[0]) as json_file:
        data_json = json.load(json_file)

    # сохраняем в переменные даты и генерацию, без нулевых показателей и с переводом значений в float
    year = tuple(i['date'] for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    generate = tuple(float(i['fields'][0]['value'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)


    # Create a dictionary
    # data = dict(zip(year, generate))
    data = pd.DataFrame({'year': year, 'generate': generate})
    data['cum_sum'] = data['generate'].cumsum()
    data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]
    finalYear = data_json['dataset']['end']  # Финальный год

    # for i in doc:
    #     os.remove(os.path.join(current_dir, i))

    metod_list = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']
    vyvod = []
    signal = True
    r = 0
    ind = 0
    sqrt_list = []
    result = {}
    for n in metod_list:

        def Bass(x, P, Q, M):
            """
            Функция расчета Prognose Sales
            x: величина Prognose Cumulative за прошлый год.
            """
            return (P*M+(Q-P)*(x))-(Q/M)*(x**2)

        # Начальные значения параметров
        popt, pcov = curve_fit(Bass, data.generate, data.Sales, bounds=(0, np.inf), method='trf', maxfev = 10000)
        p0 = popt[0]
        q0 = popt[1]
        m0 = popt[2]

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

        # Готовим данные для минимизации
        k0 = [p0, q0, m0]  # Начальные значения параметров
        kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

        # Минимизируем сумму квадратов
        try:
            res = minimize(squareMistake, k0, args=generate, method=n, bounds=kb)
        except:
            continue

        if not res.success:
            print(f'Методу {n} Не удалось минимизировать функцию!')

        k = tuple(res.x)  # Получаем кортеж параметров (P, Q, M)
        print(f'значения параметров для метода {n} - {k}')

        # Готовим данные для расчета прогнозов
        years2 = [year[0]]  # Задаем начальный год
        prSales = [0]  # Задаем начальный Prognose Sales
        prCumul = [generate[0]]  # Задаем начальный Prognose Cumulative

        # Рассчитываем для всех лет
        while years2[-1] < finalYear:
            years2.append(years2[-1]+1)  # Год
            prSales.append(Bass(prCumul[-1], P=k[0], Q=k[1], M=k[2]))  # Prognose Sales
            prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative

        result[n] = {'years2':years2, 'prCumul':prCumul}

        # метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
        def rss(y_real, y_predicted):
            """Метрика суммы квадратов остатков, Результат должен быть наименьшим.
            """
            squared_residuals = np.square(np.subtract(y_real, y_predicted))
            return sum(squared_residuals)

        data['prCumul'] = prCumul[:len(generate)]
        y_real = data['generate']
        y_predicted = data['prCumul']
        sqrt_list.append([f'{n}', res.success, rss(y_real, y_predicted)])

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
    def copy_and_rename_json_file(original_file_path, new_file_name):
        # Извлечение имени файла из начального пути к нему
        original_file_name = os.path.basename(original_file_path)

        # Путь к новому файлу
        new_file_path = os.path.join(os.path.dirname(original_file_path), new_file_name)

        # Копирование файла и сохранение с новым именем
        shutil.copy(original_file_path, new_file_path)

        # Возвращение нового имени файла
        return new_file_name

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


start_time = time.time()
main()
end_time = time.time()
total_time = end_time - start_time
print(f'Время выполнения: {total_time} seconds')