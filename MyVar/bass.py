import json
import sys
from scipy.optimize import minimize
from matplotlib import pyplot

# Начальные значения параметров
p0 = 0.0000006  # P
q0 = 0.8  # Q
m0 = 20 # M

finalYear = 2050  # Финальный год

fileIn = 'inputCIS.json'  # Имя входного json-файла
fileOut = 'output.json'  # Имя выходного json-файла


def prognose(k: tuple, c: float) -> float:
    """
    Функция расчета Prognose Sales

    k: кортеж параметров (P, Q, M);
    c: величина Prognose Cumulative за прошлый год.
    """
    return k[0]*k[2] + (k[1]-k[0])*c - (k[1]/k[2])*c**2


def goal(k: tuple, *sales) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.

    k: кортеж параметров (P, Q, M);
    sales: кортеж Sales.
    """
    # Начальные значения для первого года
    p0 = 0  # Prognose Sales
    c0 = sales[0]  # Prognose Cumulative

    res = 0  # Значение функции

    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        p = prognose(k, c0)  # Новый Prognose Sales
        c = c0 + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем

        # Обновляем значения
        p0 = p
        c0 = c

    return res


# Читаем входной json-файл
with open(fileIn, 'r') as f:
    dataIn = json.load(f)

# Формируем данные по годам
years1 = tuple(dataIn['year'])
gens = tuple(dataIn['generate'])

# Готовим данные для минимизации
k0 = [p0, q0, m0]  # Начальные значения параметров
kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

# Минимизируем сумму квадратов
res = minimize(goal, k0, args=gens, method='Nelder-Mead', bounds=kb)

# При неудачной минимизации сообщаем и выходим
if not res.success:
    print('Не удалось минимизировать функцию.')
    sys.exit()

k = tuple(res.x)  # Получаем кортеж параметров (P, Q, M)

# Готовим данные для расчета прогнозов
years2 = [years1[0]]  # Задаем начальный год
prSales = [0]  # Задаем начальный Prognose Sales
prCumul = [gens[0]]  # Задаем начальный Prognose Cumulative

# Рассчитываем для всех лет
while years2[-1] < finalYear:
    years2.append(years2[-1]+1)  # Год
    prSales.append(prognose(k, prCumul[-1]))  # Prognose Sales
    prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative

# Формируем структуру выходных данных
dataOut = {}
dataOut['param'] = {'P': k[0], 'Q': k[1], 'M': k[2]}  # Параметры
dataOut['year'] = years2  # Года
dataOut['prSales'] = prSales  # Значения Prognose Sales
dataOut['prCumul'] = prCumul  # Значения Prognose Cumulative

# Записываем выходной json-файл
with open(fileOut, 'w') as f:
    f.write(json.dumps(dataOut))

# Выводим коэффициенты
print('Коэффициенты:')
print('P =', k[0])
print('Q =', k[1])
print('M =', k[2])

# Выводим графики для контроля
pyplot.plot(years1, gens, label='Sales fact')  # Исходный
pyplot.plot(years2, prCumul, label='Sales Bass')  # Расчитанный
pyplot.xlabel('year')  # Заголовок оси Х
pyplot.ylabel('generate')  # Заголовок оси Y
pyplot.legend()  # Отображаем имена данных
pyplot.show()  # Отображаем график
