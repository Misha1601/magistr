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
    df.to_sql('Wind', conn, if_exists='replace', index=False)

    # Закрытие соединения с базой данных
    conn.close()

xlsx_to_sqlite('Wind.xlsx')

# Подключаемся к базе данных (или создаем новую, если она не существует)
conn = sqlite3.connect('Wind.db')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Начинаем строить SQL-запрос для создания таблицы
create_table_query = '''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    prognos TEXT NOT NULL,
    step INTEGER NOT NULL,
    model TEXT NOT NULL,
    metod TEXT NOT NULL,
    param TEXT NOT NULL,
    param0 TEXT NOT NULL,
    year_test INTEGER,
    data_origin REAL,
    data_prognos REAL,
    otcloneni REAL,
    MAE REAL,
    MAE_pribl REAL,
'''

# Добавляем поля для каждого года от 1995 до 2073
for year in range(1995, 2074):
    create_table_query += f'    "{year}" TEXT,\n'

# Закрываем SQL-запрос
create_table_query = create_table_query.rstrip(',\n') + '\n);'

# Выполняем SQL-запрос
cursor.execute(create_table_query)

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()

print("Таблица успешно создана")