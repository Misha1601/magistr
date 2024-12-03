import plotly.graph_objs as go
import plotly.offline as pio
import numpy as np
from django.shortcuts import render, redirect
from .forms import WindForm

def generate_plots(form_data):
    bass_plots = {}
    logic_plots = {}
    gompertz_plots = {}

    bass_models = ['Bass1', 'Bass2', 'Bass3']
    logic_models = ['Logic1', 'Logic2', 'Logic3']
    gompertz_models = ['Gompertz1', 'Gompertz2', 'Gompertz3']

    for model in form_data['models']:
        x = np.linspace(0, 10, 100)

        if model in bass_models:
            y1 = np.sin(x + np.random.random())
            y2 = np.cos(x + np.random.random())
            bass_plots[model] = [
                {
                    'x': x.tolist(),
                    'y': y1.tolist(),
                    'name': 'Кривая 1',
                    'visible': True
                },
                {
                    'x': x.tolist(),
                    'y': y2.tolist(),
                    'name': 'Кривая 2',
                    'visible': True
                }
            ]

        elif model in logic_models:
            y1 = np.exp(x / 5) / (1 + np.exp(x / 5))
            y2 = np.log(x + 1)
            logic_plots[model] = [
                {
                    'x': x.tolist(),
                    'y': y1.tolist(),
                    'name': 'Кривая 1',
                    'visible': True
                },
                {
                    'x': x.tolist(),
                    'y': y2.tolist(),
                    'name': 'Кривая 2',
                    'visible': True
                }
            ]

        else:  # Gompertz models
            y1 = np.exp(-np.exp(-x))
            y2 = x ** 0.5
            gompertz_plots[model] = [
                {
                    'x': x.tolist(),
                    'y': y1.tolist(),
                    'name': 'Кривая 1',
                    'visible': True
                },
                {
                    'x': x.tolist(),
                    'y': y2.tolist(),
                    'name': 'Кривая 2',
                    'visible': True
                }
            ]

    return bass_plots, logic_plots, gompertz_plots

def index(request):
    form = WindForm()
    return render(request, 'main/index.html', {'form': form})

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