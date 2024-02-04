import json
import os
import shutil
import pandas as pd
import numpy as np
from matplotlib import pyplot
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

    if 'Prognose_Request.json' not in doc:
        print('no file')
        return None

    js_file = [os.path.join(current_dir, 'Prognose_Request.json')]

    # Считываем JSON file
    with open(js_file[0]) as json_file:
        data_json = json.load(json_file)

    # сохраняем в переменные даты и генерацию, без нулевых показателей и с переводом значений в float
    year = tuple(i['date'] for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    generate = tuple(float(i['fields'][0]['value'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)


    # Создаем DataFrame
    # data = dict(zip(year, generate))
    data = pd.DataFrame({'year': year, 'generate': generate})
    # data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    #                  'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]})

    # Получаем список индесов
    indexdata = list(data.index.values)
    # Получаем первоночальное значение генерации
    data0 = data['generate'][0]

    # Получаем в переменную финальный год
    finalYear = data_json['dataset']['end']

    # если необходимо удаление файла в папке
    # for i in doc:
    #     os.remove(os.path.join(current_dir, i))

    # Помещаем в список все методы, которые необходимо перебрать
    metod_list = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr']
    # r = 0
    # ind = 0
    sqrt_list = []
    result = {}
    def Gompertz(n, B, C, M):
        """
        Функция расчета Prognose Sales
        x: величина Prognose Cumulative за прошлый год.
        """
        return data0 + (M) * (np.exp(-np.exp(B - C * n)))

    def squareMistake(k: tuple, *sales) -> float:
        """
        Функция для минимизации через scipy.
        Рассчитывает сумму квадратов разностей значений
        Prognose Cumulative и Prognose Sales.
        k: кортеж начальных параметров (B, C, M);
        sales: кортеж Sales.
        """
        # Начальные значения для первого года
        p0 = 0  # Prognose Sales
        c0 = sales[0]  # Prognose Cumulative
        res = 0  # Значение функции
        # Набираем результат функции за годы
        for i in range(1, len(sales)):
            p = Gompertz(i, B=k[0], C=k[1], M=k[2])  # Новый Prognose Sales
            res += (p - sales[i])**2  # Добавляем
        return res

    # Начальные значения параметров
    popt, pcov = curve_fit(Gompertz, indexdata[1:], data.generate[1:], bounds=(0, np.inf), method='trf', maxfev = 10000)
    b0 = popt[0]
    c0 = popt[1]
    m0 = popt[2]

    # Выводим стартовые коэффициенты
    print('Стартовые коэффициенты:')
    print('B0 =', b0)
    print('C0 =', c0)
    print('M0 =', m0)

    # Перебираем каждый из методов
    for n in metod_list:
        # Готовим данные для минимизации
        k0 = [b0, c0, m0]  # Начальные значения параметров
        kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

        # Минимизируем сумму квадратов
        try:
            res = minimize(squareMistake, k0, args=generate, method=n, bounds=kb)
        except:
            continue

        if not res.success:
            print(f'Методу {n} Не удалось минимизировать функцию!')

        k = tuple(res.x)  # Получаем кортеж параметров (B, C, M)
        print(f'значения параметров для метода {n} - {k}')

        # Готовим данные для расчета прогнозов
        years2 = [year[0]]  # Задаем список лет, указав начальный год
        prSales = [0]  # Задаем начальный Prognose
        prCumul = 1  # Задаем начальный порядковый номер

        # Рассчитываем для всех лет
        while years2[-1] < finalYear:
            years2.append(years2[-1]+1)  # Добавляем следующий год
            prSales.append(Gompertz(prCumul, B=k[0], C=k[1], M=k[2]))  # Добавляем следующий Prognose
            prCumul += 1  # Увеличиваем порядковый номер

        # Записываем в словарь полученные значения
        result[n] = {'years2':years2, 'prSales':prSales}

        # метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
        def rss(y_real, y_predicted):
            """Метрика суммы квадратов остатков, Результат должен быть наименьшим.
            """
            squared_residuals = np.square(np.subtract(y_real, y_predicted))
            return sum(squared_residuals)

        data['prSales'] = prSales[:len(generate)]
        y_real = data['generate']
        y_predicted = prSales[:len(generate)]
        # Записываем сумму разницы квадратов для каждого метода
        sqrt_list.append([f'{n}', res.success, rss(y_real, y_predicted)])

        # Выводим графики для контроля
        pyplot.plot(year, generate, label='Sales fact')  # Исходный
        pyplot.plot(years2, prSales, label='Sales Gompertz')  # Расчитанный
        pyplot.xlabel('year')  # Заголовок оси Х
        pyplot.ylabel('generate')  # Заголовок оси Y
        pyplot.legend()  # Отображаем имена данных
        # pyplot.show()  # Отображаем график

    # В переменную записываем метод с наименьшей суммой разницы квадратов
    n = []
    for i in sqrt_list:
        # print(i)
        if len(n) == 0:
            n = i
            continue
        if i[2] < n[2]:
            n = i
    print(f'Наменьшая сумма разницы квадратов у - {n[0]}')

    # Создаем словарь с значениями n
    data2 = dict(zip(result[n[0]]['years2'], result[n[0]]['prSales']))

    def copy_and_rename_json_file(original_file_path, new_file_name):
        """Копируем исходный json и переименовываем
        """
        # Извлечение имени файла из начального пути к нему
        original_file_name = os.path.basename(original_file_path)

        # Путь к новому файлу
        new_file_path = os.path.join(os.path.dirname(original_file_path), new_file_name)

        # Копирование файла и сохранение с новым именем
        shutil.copy(original_file_path, new_file_path)

        # Возвращение нового имени файла
        return new_file_name

    # Создание переменной с именем нового файла
    file_name = 'dataOut.json'
    # Создаем копию исходного файла и переименовываем
    copy_and_rename_json_file(js_file[0], file_name)

    # Проверяем ключи сгенерированных данных с ключами в скопированном словаре,
    # если они есть обновляем, если нет, добавляем
    for key, value in data2.items():
        for i in data_json['dataset']['records']:
            if i['date'] == key:
                i['fields'][0]['value'] = str(value)
                break
        else:
            data_json['dataset']['records'].append({'date':key, 'fields':[{'name': "Generation wind world", "datatype": "double", 'value':str(value)}]})

    # Записываем в json обновленные данные
    with open('dataOut.json', 'w') as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)


start_time = time.time()
main()
end_time = time.time()
total_time = end_time - start_time
print(f'Время выполнения: {total_time} seconds')