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
            result_dict[country][year_full[-1]] = year_full_int, predicted_values
        else:
            predicted_data = new_df[filtered_columns_wind].astype(float)
            year_full = [col for col in new_df.columns if col.isdigit() and len(col) == 4 and int(col)<=int(row.last_valid_index())]
            year_full_int = [int(i) for i in year_full]
            predicted_values = [i for i in new_df[year_full].astype(float).values[0] if i != None]
            result_dict[country][year_full[-1]] = year_full_int, predicted_values
    return result_dict


if __name__ == '__main__':
    # Пример использования функции
    name_strana  = 'Canada'
    models = ['Bass1', 'Bass2', 'Bass3', 'Logic1', 'Logic2', 'Logic3', 'Gompertz1', 'Gompertz2', 'Gompertz3']
    p = 30
    for k in models:
        strana = analyze_data(name_strana, p, '-', k, 'Nelder-Mead')
        # print(strana)

        plt.figure(figsize=(10, 6))
        for i in strana[name_strana].keys():
            if i == 'origen':
                plt.plot(strana[name_strana][i][0], strana[name_strana][i][1], label=f'Оригинальные данные')
            else:
                # print(i)
                plt.plot(strana[name_strana][i][0], strana[name_strana][i][1], label=f"Предсказанные данные до {i}") #, {strana[name_strana][i][2]}, {strana[name_strana][i][3]}")
        if p >= 6:
            strana2 = analyze_data(name_strana, 5, 5, k, 'Nelder-Mead')
            for n in strana2[name_strana].keys():
                if n == 'origen':
                    continue
                plt.plot(strana2[name_strana][n][0], strana2[name_strana][n][1], label=f"Предсказанные данные до {n}")

        plt.xlabel('Год')
        plt.ylabel('KW')
        plt.title(f'Модель {k}')
        plt.legend(loc='upper right', bbox_to_anchor=(0.3, 1.15))
        # Настройка ориентации меток на оси X
        plt.xticks(rotation=90)
        plt.show()