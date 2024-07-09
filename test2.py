import openpyxl
import pandas as pd
import numpy as np

def parser_xmlx(xmlx_file):
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

    # Создаем DataFrame из полученных данных
    data = pd.DataFrame({'year': year, 'generate': generate, 'total': total, 'costs': costs})
    data['cum_sum'] = data['generate'].cumsum()
    data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]
    data['data0'] = data['generate'][0]

    print(data)
    print(list(data['year'])[-1])

    return data

parser_xmlx('Prognose_Request.xlsx')