import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

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
# df.to_excel('WindDB_results.xlsx', index=False)

print("Данные успешно экспортированы")

def merge_tables_to_xlsx():
    # Подключение к БД
    conn = sqlite3.connect('Wind.db')

    # Получаем данные из таблиц
    wind_df = pd.read_sql_query("SELECT * FROM Wind", conn)
    results_df = pd.read_sql_query("SELECT * FROM results", conn)

    conn.close()

    # Переименовываем колонку Country в таблице Wind для соответствия с results
    wind_df = wind_df.rename(columns={'Country': 'country'})

    # Объединяем DataFrame вертикально
    merged_df = pd.concat([results_df, wind_df], axis=0)

    merged_df = merged_df[[merged_df.columns[-1]] + merged_df.columns.tolist()[1:-1]]

    # Генерируем имя файла с текущей датой
    filename = f'merged_wind_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    # Сохраняем в Excel
    merged_df.to_excel(filename, index=False, engine='openpyxl')

    return filename

# Запускаем функцию
if __name__ == "__main__":
    merge_tables_to_xlsx()