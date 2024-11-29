import sqlite3
import pandas as pd
import numpy as np

# Подключение к базе данных SQLite
conn = sqlite3.connect('Wind.db')

# Запрос для извлечения данных
query = 'SELECT * FROM Wind'

# Чтение данных в DataFrame
df = pd.read_sql_query(query, conn)

# Закрытие соединения с базой данных
conn.close()

# Преобразование всех строк в числовой формат
for column in df.columns:
    # Попытка преобразования значений в числовой формат
    numeric_values = pd.to_numeric(df[column], errors='coerce')
    # Замена значений только там, где преобразование удалось
    df[column] = df[column].where(numeric_values.isna(), numeric_values)

# Экспорт DataFrame в файл Excel
df.to_excel('WindDB_Wind.xlsx', index=False)

print("Данные успешно экспортированы в output.xlsx")

t1 = [0.059000000000000004, 0.08251346764912308, 0.11535160091887517, 0.1611681566958683, 0.22500664299506717, 0.31378916301880483, 0.43693935878360884, 0.6071389774231399, 0.8411733991680183, 1.1607299284688934, 1.5928448085396185, 2.169424455956841, 2.9249067247763847, 3.8908201757549, 5.086154637440367, 6.50383747743764, 8.096950077221301, 9.772896950639801, 11.405423241853565]
t2 = [0.059000000000000004, 0.0819281569509494, 0.11374798964621079, 0.157890585906732, 0.21909511837384688, 0.3038928424013748, 0.4212565557388246, 0.5834593332734532, 0.807185438943573, 1.114920249817806, 1.5365981386014318, 2.111378905480822, 2.8892104328484263, 3.931461991062641, 5.309339247873698, 7.098078820418711, 9.364408753134489, 12.14533502179492, 15.419467313463706]
mae2 = np.mean(np.abs(np.array(t1) - np.array(t2)))
print(mae2)
print(list(np.array(t1) - np.array(t2)))
print(np.array(t1) - np.array(t2))
print([i*i for i in list(np.array(t1) - np.array(t2))])
print(np.abs(np.array(t1) - np.array(t2)))
# print(np.mean([i*i for i in list(np.array(t1) - np.array(t2))]))