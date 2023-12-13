import pandas as pd
import os.path
import openpyxl

def read_xlsx_as_rows(file_path):
    """Создаем датафрэйм их экселя"""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Пример использования:
# Конвертируем эксель в датафрэйм
file_path = 'output_myvar.xlsx'
result_df = read_xlsx_as_rows(file_path)

# ВЫбираем уникальные значения из столбцов
strana = result_df['strana'].unique()
region = result_df['region'].unique()
# выводим заголовок, 0 строку, на печать в виде списка
unique_tolist = result_df.columns.tolist()
print(strana[0])
print(region[0])
print(unique_tolist)
# вывод строки по индексу с 0, где заголовок метка
# print(result_df.loc[[2]])

# получаем список стран использующий ветрогенерацию
wind_strana = [i[2] for i in result_df.loc[result_df['energe'] == 'WindGeneration-TWh'].values.tolist()]

# перебираем список регионов, 2 столбец
for i in region:
    # перебираем список стран, 3 столбец
    for k in strana:
        # проверяем данная страна производит ветрогенерацию или нет
        if k in wind_strana:
            # сохраняем список индексов для страны по всему датафрэйму
            indices = result_df.loc[(result_df['region'] == i) & (result_df['strana'] == k)].index
            # вводим переменную, с которой начнём вводить данные в новый эксель
            indstr = 2
            # print(indices)
            # перебираем все индексы
            for n in indices:
                # print(result_df.loc[[n]].values.tolist()[0][2], result_df.loc[[n]].values.tolist()[0][1],
                # result_df.loc[[n]].values.tolist()[0][0])
                # проверяем наличие файла, если его нету, создаем иначе открываем
                if not os.path.isfile('output_df_xlsx.xlsx'):
                    wb = openpyxl.Workbook()
                else:
                    wb = openpyxl.load_workbook('output_df_xlsx.xlsx')
                # print(wb.sheetnames)
                # проверяем, лист с именем страны
                if result_df.loc[[n]].values.tolist()[0][2] not in wb.sheetnames:
                    # создаем лист
                    wb.create_sheet(title=f'{result_df.loc[[n]].values.tolist()[0][2]}')
                    # переключаемся на этот лист
                    sheet = wb[f'{result_df.loc[[n]].values.tolist()[0][2]}']
                    # в первую ячейку вводим страну
                    sheet.cell(row=1, column=1, value=f'{result_df.loc[[n]].values.tolist()[0][2]}')
                    # во вторую ячейку - регион
                    sheet.cell(row=1, column=2, value=f'{result_df.loc[[n]].values.tolist()[0][1]}')
                    # в следующую строку год и в остальные ячейки этой строки значения каждого года
                    sheet.cell(row=indstr, column=1, value='Год')
                    b = 2
                    for m in unique_tolist[3:]:
                        sheet.cell(row=indstr, column=b, value=m)
                        b += 1
                # активируем лист с страной
                sheet = wb[f'{result_df.loc[[n]].values.tolist()[0][2]}']
                # переходим к следующей строке
                indstr += 1
                # циклически в строку вводим вид генерации и их значения
                sheet.cell(row=indstr, column=1, value=f'{result_df.loc[[n]].values.tolist()[0][0]}')
                b = 2
                for m in result_df.loc[[n]].values.tolist()[0][3:]:
                    sheet.cell(row=indstr, column=b, value=m)
                    b += 1
                # Сохраняем и закрываем книгу
                wb.save('output_df_xlsx.xlsx')
                wb.close()

                # break
            break


