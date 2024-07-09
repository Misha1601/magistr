from sklearn.linear_model import LinearRegression
import json
import os
import shutil
import pandas as pd
import numpy as np
import datetime
import openpyxl
# from scipy.optimize import minimize
# from scipy.optimize import curve_fit
# import time
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def parser_json():
    # Получаем имя текущей директории и наличие файла Prognose_Request.json
    current_dir = os.getcwd()
    directory = str(current_dir)
    files = os.listdir(directory)
    doc = list(filter(lambda x: x[-5:] == '.json', files))
    if 'Prognose_Request.json' not in doc:
        with open('error.txt', 'w') as file:
            file.write('файл не найден')
        return None

    js_file = [os.path.join(current_dir, 'Prognose_Request.json')]

    # Считываем  JSON file
    with open(js_file[0]) as json_file:
        data_json = json.load(json_file)

    # сохраняем в переменные, без нулевых показателей и с переводом значений в float
    year = tuple(i['date'] for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    generate = tuple(float(i['fields'][0]['value'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    total = tuple(float(i['fields'][0]['total'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    costs = tuple(float(i['fields'][0]['costs'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)

    # Создаем DataFrame из полученных данных
    data = pd.DataFrame({'year': year, 'generate': generate, 'total': total, 'costs': costs})
    data['cum_sum'] = data['generate'].cumsum()
    data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]
    data['data0'] = data['generate'][0]

    # Считываем финальный год
    finalYear = data_json['dataset']['end']

    # Копируем исходный файл под новым именем
    file_name = 'dataOut.json'
    shutil.copy(js_file[0], file_name)

    return data, finalYear

def parser_xmlx(xmlx_file):
    # Необходимо доработать!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Получаем имя текущей директории и наличие файла Prognose_Request.xlsx
    # current_dir = os.getcwd()
    # directory = str(current_dir)
    # files = os.listdir(directory)
    # doc = list(filter(lambda x: x[-5:] == '.xlsx', files))
    # if 'Prognose_Request.xlsx' not in doc:
    #     with open('error.txt', 'w') as file:
    #         file.write('файл не найден')
    #     return None

    # xmlx_file = [os.path.join(current_dir, 'Prognose_Request.xlsx')]

    # Считываем  xmlx file
    # with open(js_file[0]) as json_file:
        # data_json = json.load(json_file)
    # Открываем файл Excel
    workbook = openpyxl.load_workbook(xmlx_file)
    # Выбираем активный лист (первый лист)
    sheet = workbook.active

    # Извлекаем значения из первых четырех строк
    year = [cell.value for cell in sheet[1]]
    generate = [cell.value for cell in sheet[2]]
    total = [cell.value for cell in sheet[3]]
    costs = [cell.value for cell in sheet[4]]

    print(year)

    # Закрываем файл
    workbook.close()

    # сохраняем в переменные, без нулевых показателей и с переводом значений в float
    # year = tuple(i['date'] for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    # generate = tuple(float(i['fields'][0]['value'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    # total = tuple(float(i['fields'][0]['total'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)
    # costs = tuple(float(i['fields'][0]['costs'].replace(',', '.')) for i in data_json['dataset']['records'] if (i['fields'][0]['value']) != 0)

    # Создаем DataFrame из полученных данных
    data = pd.DataFrame({'year': year, 'generate': generate, 'total': total, 'costs': costs})
    data['cum_sum'] = data['generate'].cumsum()
    data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]
    data['data0'] = data['generate'][0]

    # Считываем финальный год
    # finalYear = data_json['dataset']['end']

    # Копируем исходный файл под новым именем
    # file_name = 'dataOut.json'
    # shutil.copy(js_file[0], file_name)

    return data

def rss(y_real, y_predicted):
    """Метрика суммы квадратов остатков, Результат должен быть наименьшим."""
    squared_residuals = np.square(np.subtract(y_real, y_predicted))
    return sum(squared_residuals)

def save_json(data2):
    # Получаем имя текущей директории и наличие файла dataOut.json
    current_dir = os.getcwd()
    directory = str(current_dir)
    files = os.listdir(directory)
    doc = list(filter(lambda x: x[-5:] == '.json', files))
    if 'dataOut.json' not in doc:
        with open('error.txt', 'w') as file:
            file.write('файл не найден')
        return None

    js_file = [os.path.join(current_dir, 'dataOut.json')]

    # Считываем  JSON file
    with open(js_file[0]) as json_file:
        data_json = json.load(json_file)

    for key, value in data2.items():
        for i in data_json['dataset']['records']:
            if i['date'] == key:
                i['fields'][0]['value'] = str(value)
                break
        else:
            data_json['dataset']['records'].append({'date':int(key), 'fields':[{'name': "Generation wind world", "datatype": "double", 'value':str(value)}]})

    with open(js_file[0], 'w') as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)

def linear_regression_extension(original_array, n):
    """
    Принимает массив и число n, применяет метод линейной регрессии и возвращает продолженный массив.

    Parameters:
    - original_array (np.array): Исходный массив данных.
    - n (int): Длина массива, который нужно получить.

    Returns:
    - np.array: Продолженный массив.
    """
    # Создаем массив индексов для исходного массива
    x = np.arange(len(original_array)).reshape(-1, 1)

    # Создаем модель линейной регрессии
    model = LinearRegression().fit(x, original_array)

    # Создаем массив индексов для новых данных
    new_x = np.arange(len(original_array), len(original_array) + n).reshape(-1, 1)

    # Предсказываем новые значения с использованием модели
    predicted_values = model.predict(new_x)

    return predicted_values

def log_error(file_name, stroca):
    with open(file_name, 'a') as file:
        file.write(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")} {stroca}\n')

def main():
    # data_total = np.array([0.196, 0.178, 0.157, 0.139, 0.134, 0.142, 0.126, 0.119, 0.106, 0.111, 0.104, 0.105, 0.098, 0.088, 0.087, 0.086, 0.083, 0.083, 0.082, 0.076, 0.069, 0.066, 0.064, 0.058, 0.053])
    # extended_array = linear_regression_extension(data_total, 5)
    # print(type(extended_array))
    # print(np.concatenate([data_total, extended_array]))
    # log_error('error.txt', "что то пошло не так")
    # log_error('error.txt', "дописал в файл")
    parser_xmlx('Prognose_Request.xlsx')

if __name__ == '__main__':
    main()