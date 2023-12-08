import openpyxl
import pandas as pd

def process_xlsx(file_path):
    try:
        workbook = openpyxl.load_workbook(file_path)
        regions_dict = {}

        for sheet in workbook.sheetnames:
            current_sheet = workbook[sheet]
            sheet = sheet.replace(" ", "")
            regions_dict[sheet] = {}

            # Находим первую непустую ячейку в столбце B
            start_row = 1
            for cell in current_sheet['B']:
                if cell.value:
                    start_row = cell.row
                    # print(start_row)
                    break

            # Находим последнюю строку с "Total World"
            end_row = 1
            for cell in current_sheet['A']:
                if cell.value == "Total World":
                    end_row = cell.row + 1
                    # print(end_row)
                    break

            for row in range(start_row, end_row):
                if row == start_row:
                    regions_dict[sheet]['data'] = [cell.value for cell in current_sheet[row][1:]]
                    continue
                if current_sheet[row][0].value:
                    regions_dict[sheet][current_sheet[row][0].value.replace(" ", "")] = [cell.value for cell in current_sheet[row][1:]]

        # Выводим словарь
        print("Словарь регионов:")
        # for region, sheet_name in regions_dict.items():
        #     print(f"{region}: {sheet_name}")

        return regions_dict

    except Exception as e:
        print(f"Error: {e}")
        return None

# Пример использования
file_path = "/home/misha/Python/magistr/Модели Excel/World Energy.xlsx"
result = process_xlsx(file_path)

if result is not None:
    reg = list(result.keys())
    # print(list(reg))
    for i in reg:
        print(f"для {i} первый год {result[i]['data'][0]}")

    my_list = []
    columns = ['region', 'strana']
    for i in range(1965, 2023):
        columns.append(i)
    # print(columns)
    for i in list(result.keys()):
        # my_list.append([i])
        for k in list(result[i].keys()):
            if k == 'data':
                continue
            my_list.append([i, k])
            sch = 0
            for n in range(1965, 2023):
                if n == result[i]['data'][sch]:
                    my_list[-1].append(result[i][k][sch])
                    sch += 1
                else:
                    my_list[-1].append(0)

    # for i in my_list:
    #     print(i)


else:
    print("Не удалось обработать файл.")

df = pd.DataFrame(my_list, columns=columns)
print(df)

# Указываем путь к файлу
file_path = 'output.xlsx'

# Записываем DataFrame в файл Excel
df.to_excel(file_path, index=False)
