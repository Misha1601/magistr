import pandas as pd
import sqlite3

def xlsx_to_sqlite(file_path):
    # Чтение xlsx файла
    df = pd.read_excel(file_path)
    print(df.iloc[0].dtypes)
    print(df.iloc[-1].dtypes)

    # Создание соединения с базой данных SQLite
    conn = sqlite3.connect('Wind.db')

    # Запись DataFrame в базу данных SQLite
    df.to_sql('data', conn, if_exists='replace', index=False)

    # Закрытие соединения с базой данных
    conn.close()

xlsx_to_sqlite('Wind.xlsx')