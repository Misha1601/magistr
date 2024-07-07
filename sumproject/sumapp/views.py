from django.shortcuts import render, redirect
from .forms import SumForm

def sum_view(request):
    if request.method == 'POST':
        form = SumForm(request.POST)
        if form.is_valid():
            num1 = form.cleaned_data['num1']
            num2 = form.cleaned_data['num2']
            num3 = form.cleaned_data['num3']
            num4 = form.cleaned_data['num4']
            result = num1 + num2 + num3 + num4
            request.session['result'] = result  # Сохраняем результат в сессии
            return render(request, 'sum.html', {'form': form, 'result': result})
    else:
        form = SumForm()
    return render(request, 'sum.html', {'form': form})

def result_view(request):
    result = request.session.get('result', None)
    return render(request, 'result.html', {'result': result})