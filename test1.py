import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Функция для анализа данных
def analyze_data(country, prognos, step, model, metod):
    """Функция для анализа данных"""
    # Извлечение данных
    conn = sqlite3.connect('Wind.db')
    query = f"SELECT * FROM Wind WHERE Country = ?"
    wind_data = pd.read_sql_query(query, conn, params=[country])
    query_p = f"SELECT * FROM results WHERE country = ? AND prognos = ? AND step = ? AND model = ? AND metod = ?"
    results_data = pd.read_sql_query(query_p, conn, params=[country, prognos, step, model, metod])
    conn.close()

    # Фильтруем столбцы, которые являются годами
    filtered_columns_wind = [col for col in wind_data.columns if col.isdigit() and len(col) == 4]

    # Обрезаем DataFrame до столбцов, которые являются годами
    # Оригинальные данные до предсказания
    original_data_wind = wind_data[filtered_columns_wind].astype(float)
    original_year = [int(i) for i in filtered_columns_wind]
    original_values = [i for i in original_data_wind.values[0]]
    len_original_values = len(original_values)
    # print(original_values)

    result_dict = {}
    result_dict[country] = {}
    result_dict[country]['origen'] = original_year, original_values

    # Анализ данных
    for index, row in results_data.iterrows():
        year_end = int(row.last_valid_index())
        year_start = year_end - prognos

        # Создаем новый DataFrame из строки
        new_df = row.to_frame().T
        # print(new_df)

        if year_end > int(filtered_columns_wind[-1]):
            # print(year_end)
            predicted_data = new_df[filtered_columns_wind].astype(float)
            year_full = [col for col in new_df.columns if col.isdigit() and len(col) == 4 and int(col)<=int(row.last_valid_index())]
            year_full_int = [int(i) for i in year_full]
            predicted_values = [i for i in new_df[year_full].astype(float).values[0] if i != None]
            if len(original_values) >= len(predicted_values):
                # Среднеквадратичное отклонение (RMSE)
                print(len(original_data_wind))
                print(len(predicted_data))
                rmse = np.sqrt(np.mean((np.array(original_values[:len(predicted_values)]) - np.array(predicted_values))**2))
                # Средняя абсолютная ошибка (MAE)
                mae = np.mean(np.abs(np.array(original_values[:len(predicted_values)]) - np.array(predicted_values)))
            else:
                # Среднеквадратичное отклонение (RMSE)
                print(len(original_data_wind))
                print(len(predicted_data))
                rmse = np.sqrt(np.mean((np.array(original_values[:len(predicted_values)]) - np.array(predicted_values[:len(original_values)]))**2))
                # Средняя абсолютная ошибка (MAE)
                mae = np.mean(np.abs(np.array(original_values[:len(predicted_values)]) - np.array(predicted_values[:len(original_values)])))
            result_dict[country][year_full[-1]] = year_full_int, predicted_values, rmse, mae
        else:
            predicted_data = new_df[filtered_columns_wind].astype(float)
            year_full = [col for col in new_df.columns if col.isdigit() and len(col) == 4 and int(col)<=int(row.last_valid_index())]
            year_full_int = [int(i) for i in year_full]
            predicted_values = [i for i in new_df[year_full].astype(float).values[0] if i != None]
            len_predicted_values = len(predicted_values)
            if len_original_values >= len_predicted_values:
                new_original_values = original_values[:len_predicted_values]
                new_predicted_values = predicted_values
            else:
                new_predicted_values = predicted_values[:len_original_values]
                new_original_values = original_values
            # print(len(new_original_values))
            # print(len(new_predicted_values))
            y_true = np.array(new_original_values)
            y_pred = np.array(new_predicted_values)

            # Среднеквадратичное отклонение (RMSE)
            rmse = np.sqrt(np.mean((y_true - y_pred)**2))
            # Средняя абсолютная ошибка (MAE)
            mae = np.mean(np.abs(y_true - y_pred))
            result_dict[country][year_full[-1]] = year_full_int, predicted_values, rmse, mae
    return result_dict



def export_tables_to_excel(db_name):
    # Подключение к базе данных
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Получение списка таблиц в базе данных
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Перебор каждой таблицы и сохранение в файл Excel
    for table in tables:
        table_name = table[0]
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        df = df.astype(float)
        df.to_excel(f"{table_name}.xlsx", index=False)
        print(f"Таблица {table_name} успешно экспортирована в {table_name}.xlsx")

    # Закрытие соединения
    conn.close()

if __name__ == '__main__':
    # Пример использования функции
    name_strana  = 'Vietnam'
    strana = analyze_data(name_strana, 5, 5, 'Bass3', 'Nelder-Mead')
    print(strana)

    # export_tables_to_excel('Wind.db')

    plt.figure(figsize=(10, 6))
    for i in strana[name_strana].keys():
        if i == 'origen':
            plt.plot(strana[name_strana][i][0], strana[name_strana][i][1], label=f'Оригинальные данные')
        else:
            # print(i)
            plt.plot(strana[name_strana][i][0], strana[name_strana][i][1], label=f"Предсказанные данные до {i}, {strana[name_strana][i][2]}, {strana[name_strana][i][3]}")
    plt.xlabel('Год')
    plt.ylabel('Значение')
    plt.title(f'Сравнение данных')
    plt.legend(loc='upper right', bbox_to_anchor=(0.65, 1.15))
    # Настройка ориентации меток на оси X
    plt.xticks(rotation=90)
    plt.show()