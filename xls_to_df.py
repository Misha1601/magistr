import pandas as pd
import os.path
import openpyxl

def read_xlsx_as_rows(file_path):
    try:
        df = pd.read_excel(file_path)
        # df_transposed = df.transpose()
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Пример использования:
file_path = 'output_myvar.xlsx'
result_df = read_xlsx_as_rows(file_path)

if result_df is not None:
    print(result_df)

strana = result_df['strana'].unique()
region = result_df['region'].unique()
unique_tolist = result_df.columns.tolist()
print(strana[0])
print(region[0])
print(unique_tolist)
# вывод строки по индексу с 0, где заголовок метка
# print(result_df.loc[[2]])

wind_strana = [i[2] for i in result_df.loc[result_df['energe'] == 'WindGeneration-TWh'].values.tolist()]


list_str = []
for i in region:
    for k in strana:
        if k in wind_strana:
            indices = result_df.loc[(result_df['region'] == i) & (result_df['strana'] == k)].index
            indstr = 2
            # print(indices)
            for n in indices:
                # list_str.append([result_df.loc[[n]]['strana'].values, result_df.loc[[n]]['region'].values, result_df.loc[[n]]['energe'].values])
                # print(result_df.loc[[n]].values.tolist()[0][2], result_df.loc[[n]].values.tolist()[0][1],
                # result_df.loc[[n]].values.tolist()[0][0])
                if not os.path.isfile('output_df_xlsx.xlsx'):
                    wb = openpyxl.Workbook()
                else:
                    wb = openpyxl.load_workbook('output_df_xlsx.xlsx')
                # print(wb.sheetnames)
                if result_df.loc[[n]].values.tolist()[0][2] not in wb.sheetnames:
                    wb.create_sheet(title=f'{result_df.loc[[n]].values.tolist()[0][2]}')
                    sheet = wb[f'{result_df.loc[[n]].values.tolist()[0][2]}']
                    sheet.cell(row=1, column=1, value=f'{result_df.loc[[n]].values.tolist()[0][2]}')
                    sheet.cell(row=1, column=2, value=f'{result_df.loc[[n]].values.tolist()[0][1]}')
                    sheet.cell(row=indstr, column=1, value='Год')
                    b = 2
                    for m in unique_tolist[3:]:
                        sheet.cell(row=indstr, column=b, value=m)
                        b += 1
                sheet = wb[f'{result_df.loc[[n]].values.tolist()[0][2]}']
                indstr += 1
                sheet.cell(row=indstr, column=1, value=f'{result_df.loc[[n]].values.tolist()[0][0]}')
                # indstr += 1
                # sheet.cell(row=indstr, column=1, value='Генерация')
                b = 2
                for m in result_df.loc[[n]].values.tolist()[0][3:]:
                    sheet.cell(row=indstr, column=b, value=m)
                    b += 1
                # indstr += 1
                wb.save('output_df_xlsx.xlsx')
                wb.close()

                # break
            # break
# for i in list_str:
#     print(i)
# my_str = result_df.loc[result_df['energe'] == 'WindGeneration-TWh'].values.tolist()

# for i in my_str:
#     print(i[2])

