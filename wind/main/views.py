import json
import plotly.graph_objs as go
import plotly.offline as pio
import numpy as np
import pandas as pd
import os
import sqlite3
import io
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import WindForm, REGIONS_COUNTRIES
from modules.Models_diffusion_innovations import execute_sql_query, func_minus_year, Bass1, Bass2, Bass3, Logic1, Logic2, Logic3, Gompertz1, Gompertz2, Gompertz3


def generate_plots(form_data):
    bass_plots = {}
    logic_plots = {}
    gompertz_plots = {}

    country = form_data['country']
    prediction = form_data['prediction']
    if prediction == '6':  # Если выбрано Other
        prediction = form_data['custom_prediction']

    models_dict = {
        'bass_models': ['Bass1', 'Bass2', 'Bass3'],
        'logic_models': ['Logic1', 'Logic2', 'Logic3'],
        'gompertz_models': ['Gompertz1', 'Gompertz2', 'Gompertz3']
    }

    def analyze_data(country, prognos, step, model, metod='Nelder-Mead'):
        """Функция для анализа данных"""
        # Получаем данные из Wind
        query_wind = f'SELECT * FROM Wind WHERE Country=?'
        wind_data = execute_sql_query(query_wind, [country])

        # Получаем данные из results
        query_results = 'SELECT * FROM results WHERE Country=? AND prognos=? AND model=? AND metod=?'
        results_data = execute_sql_query(query_results, [country, prognos, model, metod])

        # Если данных нет в results, вызываем func_minus_year
        if not results_data:
            for i in [Bass1, Bass2, Bass3, Logic1, Logic2, Logic3, Gompertz1, Gompertz2, Gompertz3]:
                if i.__name__ == model:
                    model1 = i
                    break
            func_minus_year(country, int(prognos), int(step), model1, metod)
            # Принудительно закрываем все соединения и создаем новое
            execute_sql_query("PRAGMA optimize", [])  # Оптимизация БД
            # Повторно запрашиваем данные
            results_data = execute_sql_query(query_results, [country, prognos, model, metod])

        # Обновляем запрос если prognos больше 5
        if int(prognos) > 5:
            query_results = 'SELECT * FROM results WHERE Country=? AND (prognos=? OR prognos="5") AND model=? AND metod=? ORDER BY prognos ASC'
            results_data = execute_sql_query(query_results, [country, prognos, model, metod])

        # Получаем список годов из структуры таблицы
        cols_query = f'PRAGMA table_info(Wind)'
        columns_info = execute_sql_query(cols_query)
        years_columns = [col[1] for col in columns_info if col[1].isdigit() and len(col[1]) == 4]

        # Получаем оригинальные данные
        original_years = [int(year) for year in years_columns]
        original_values = [float(val) for val in wind_data[0][2:] if val != '-']

        result_dict = {country: {'origen': (original_years, original_values)}}

        # Обработка результатов прогноза
        if results_data:
            for row in results_data:
                # Фильтруем годы из результатов
                years_data = []
                values_data = []

                # Пропускаем первые столбцы с метаданными
                for i, value in enumerate(row[16:]):  # Пропускаем первые 15 колонок с метаданными
                    # print(row[15:])
                    try:
                        float_value = float(value)
                        years_data.append(original_years[0] + i)
                        values_data.append(float_value)
                    except (ValueError, TypeError):
                        continue

                if years_data:
                    result_dict[country][str(years_data[-1])] = (years_data, values_data)
        # print(result_dict)
        return result_dict

    # Генерация графиков для каждой модели
    for model in form_data['models']:
        data = analyze_data(country, prediction, prediction, model)

        # Создаем список точек для графика
        traces = []
        for key, values in data[country].items():
            trace = {
                'x': values[0],  # года
                'y': values[1],  # значения
                'name': 'Оригинальные данные' if key == 'origen' else f'Предсказание до {key}',
                'visible': True
            }
            traces.append(trace)

        # Добавляем график в соответствующий словарь
        if model in models_dict['bass_models']:
            bass_plots[model] = traces
        elif model in models_dict['logic_models']:
            logic_plots[model] = traces
        else:  # Gompertz models
            gompertz_plots[model] = traces

    return bass_plots, logic_plots, gompertz_plots

def index(request):
    form = WindForm()
    # Передаем словарь регионов и стран в шаблон
    context = {
        'form': form,
        'regions_countries': json.dumps(REGIONS_COUNTRIES)
    }
    return render(request, 'main/index.html', context)

def process_form(request):
    if request.method == 'POST':
        form = WindForm(request.POST)
        if form.is_valid():
            # Сохраняем данные формы в сессии
            request.session['form_data'] = form.cleaned_data
            return redirect('plot_view')

    return index(request)

def plot_view(request):
    # Получаем данные из сессии
    form_data = request.session.get('form_data')

    if not form_data:
        return redirect('index')

    bass_plots, logic_plots, gompertz_plots = generate_plots(form_data)

    # Создание интерактивных plotly графиков
    bass_plot_html = {}
    logic_plot_html = {}
    gompertz_plot_html = {}

    for plot_dict, html_dict in [
        (bass_plots, bass_plot_html),
        (logic_plots, logic_plot_html),
        (gompertz_plots, gompertz_plot_html)
    ]:
        for plot_name, plot_data in plot_dict.items():
            fig = go.Figure()
            for curve in plot_data:
                fig.add_trace(go.Scatter(
                    x=curve['x'],
                    y=curve['y'],
                    name=curve['name'],
                    visible=curve['visible']
                ))
            html_dict[plot_name] = pio.plot(fig, output_type='div')

    return render(request, 'main/plot.html', {
        'bass_plots': bass_plot_html,
        'logic_plots': logic_plot_html,
        'gompertz_plots': gompertz_plot_html,
        'form_data': form_data
    })

def export_excel(request):
    # Получаем данные формы из сессии
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('index')

    # Генерируем данные графиков
    bass_plots, logic_plots, gompertz_plots = generate_plots(form_data)

    # Собираем все модели в один словарь
    all_plots = {}
    all_plots.update(bass_plots)
    all_plots.update(logic_plots)
    all_plots.update(gompertz_plots)

    # Собираем все годы из всех трасс
    all_years = set()
    for model_name, plot_data in all_plots.items():
        for trace in plot_data:
            all_years.update(trace['x'])

    all_years = sorted(all_years)

    # Создаем Excel файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"

    # Заголовки: теперь вместо "Name" будет два столбца "Модель" и "Предсказания"
    header = ["Модель", "Предсказания"] + [str(year) for year in all_years]
    ws.append(header)

    # Заполняем данные
    for model_name, plot_data in all_plots.items():
        for trace in plot_data:
            # Формируем имя ряда
            model_col = model_name
            prediction_col = trace['name']

            # Сопоставляем год -> значение
            year_value_map = {y: val for y, val in zip(trace['x'], trace['y'])}

            # Строим итоговую строку
            row = [model_col, prediction_col]
            for year in all_years:
                val = year_value_map.get(year, None)
                row.append(val)

            ws.append(row)

    # Сохраняем и возвращаем файл
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    return response

def export_bd_excel(request):
    if request.method != 'POST':
        return redirect('plot_view')

    try:
        # Путь к базе данных Wind.db
        db_path = os.path.join(settings.BASE_DIR, 'modules', 'Wind.db')
        print(os.path.dirname(__file__))

        # Подключение к БД и Получаем данные из таблиц
        conn = sqlite3.connect(db_path)
        wind_df = pd.read_sql_query("SELECT * FROM Wind", conn)
        results_df = pd.read_sql_query("SELECT * FROM results", conn)
        conn.close()

        # Переименовываем колонку Country в таблице Wind для соответствия с results
        wind_df = wind_df.rename(columns={'Country': 'country'})

        # Объединяем DataFrame вертикально
        merged_df = pd.concat([results_df, wind_df], axis=0)

        # Заменяем первый столбец последним
        merged_df = merged_df[[merged_df.columns[-1]] + merged_df.columns.tolist()[1:-1]]

        # Преобразование всех строк в числовой формат
        for column in merged_df.columns:
            # Попытка преобразования значений в числовой формат
            numeric_values = pd.to_numeric(merged_df[column], errors='coerce')
            # Замена значений только там, где преобразование удалось
            merged_df[column] = merged_df[column].where(numeric_values.isna(), numeric_values)

        # Создание Excel файла в памяти
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            merged_df.to_excel(writer, index=False, sheet_name='MergedData')

        # Возвращение файла в ответе
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Wind_Results_Merged.xlsx"'
        return response

    except Exception as e:
        return HttpResponse(f"Произошла ошибка при экспорте данных: {str(e)}", status=500)