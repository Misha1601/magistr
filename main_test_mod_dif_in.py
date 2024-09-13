from Models_diffusion_innovations import *
from Functions import parser_json
from Functions import rss
from Functions import save_json
from Functions import linear_regression_extension
from Functions import log_error

# import json
# import os
# import shutil
from pprint import pprint
import pandas as pd
import numpy as np
from matplotlib import pyplot
import openpyxl
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
import time
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    workbook = openpyxl.load_workbook('xlsxtest.xlsx')
    sheet = workbook.active
    year = [cell.value for cell in sheet[1]]
    generate = [cell.value for cell in sheet[2]]
    total = [cell.value for cell in sheet[3]]
    costs = [cell.value for cell in sheet[4]]
    workbook.close()
    data = pd.DataFrame({'year': year, 'generate': generate, 'total': total, 'costs': costs})
    # print(data.year)


    pyplot.plot(data.year, data.generate, label='Sales fact')  # Исходный

    # на сколько лет вперед предсказываем
    numberP = 5

    # какой шаг используем по годам
    numberS = 2

    # количество исследований
    numberI = 3

    finalYear = list(data.year)[-1] + numberP
    # print(data)
    result = func_dif_innov(data, finalYear, Bass1)
    results = {}
    results[f'result{finalYear}'] = result[0]
    pyplot.plot(result[1], result[0], label=f'result{finalYear}')
    k = 1
    while True:
        data1 = data[:-numberS]
        finalYear = list(data1.year)[-1] + numberP
        # print(list(data1.year)[-1], finalYear)
        result = func_dif_innov(data1, finalYear, Bass1)
        if result:
            results[f'result{finalYear}'] = result[0]
            pyplot.plot(result[1], result[0], label=f'result{finalYear}')
        else:
            break
        k += 1
        numberS *= k
    print(results)




    # pyplot.plot(data.year, data.generate, label='Sales fact')  # Исходный
    # pyplot.plot(data.year, prCumul, label=f'Sales {model_func.__name__}')
    # pyplot.plot(years2, prCumul, label=f'Sales {model_func.__name__}')  # Расчитанный
    # pyplot.xlabel(list(data.year))  # Заголовок оси Х
    # pyplot.ylabel(list(data.generate))  # Заголовок оси Y
    pyplot.legend()  # Отображаем имена данных
    pyplot.show()  # Отображаем график


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} seconds')