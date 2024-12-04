import sqlite3
import pandas as pd
import numpy as np

# Подключение к базе данных SQLite
conn = sqlite3.connect('Wind.db')

# Запрос для извлечения данных
query = 'SELECT * FROM results'

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
df.to_excel('WindDB_results.xlsx', index=False)

print("Данные успешно экспортированы")
