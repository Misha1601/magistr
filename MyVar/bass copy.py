import json
import sys
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from matplotlib import pyplot

# определяем DataFrame Мировой
data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                     'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]})

# определяем DataFrame Европа
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [3.86302920121212, 4.82858524525252, 7.29549295555556, 11.1764791351515, 14.2443217667677, 22.4547142028283, 26.9342866553535, 36.4259493147475, 44.5311522856566, 59.296786859596, 71.0967493651913, 83.1641398783648, 105.713193767021, 121.353901497536, 135.383228613187, 153.443496864175, 186.657403230905, 215.032405064032, 248.115255753321, 264.815019959907, 318.931230019458, 322.867876348302, 384.216521406329, 403.217594774174, 460.029812809329, 510.138071007773]})

# определяем DataFrame Северная америка
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [3.26221515151515, 3.33473636363636, 3.39524747474747, 3.13325858585859, 4.71233131313131, 5.93275858585859, 7.15238484848485, 10.8848686868687, 12.0094707070707, 15.2516070707071, 19.5614535353535, 29.3507141414141, 38.0231120606061, 59.9658373737374, 81.8704608585859, 105.571632323232, 133.227399166667, 157.24394260101, 184.865083282828, 202.73345020202, 228.356483611111, 270.596628055556, 299.004805909091, 321.654747474747, 348.257532336614, 396.728298131659]})

# определяем DataFrame Центральная и Южная америка
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [0.00777777777777778, 0.0419739852222222, 0.102925997979798, 0.111372380198889, 0.148471920316465, 0.252114795739394, 0.320991025326263, 0.458866738412121, 0.44309745380303, 0.543414491936364, 0.532301140512121, 0.773789270347576, 1.16145997464749, 1.6704335559914, 2.07792761282224, 3.44912776667099, 4.32435901479341, 7.80414735195275, 10.1969105470833, 18.5816815022246, 31.4603868218231, 45.1770034913969, 56.1317767046775, 65.7589869448652, 78.7649400881846, 85.4184260493074]})

# определяем DataFrame CIS
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0019, 0.0031, 0.0062, 0.0086, 0.00801010101010101, 0.0078, 0.0088, 0.0105, 0.0081, 0.0112, 0.009786, 0.012539, 0.018116, 0.0211217, 0.1256712, 0.3290593, 0.5239033, 0.6069637, 0.8290751, 1.3396434, 2.59858862101087]})

# data = pd.DataFrame({'year': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [0.0019, 0.0031, 0.0062, 0.0086, 0.00801010101010101, 0.0078, 0.0088, 0.0105, 0.0081, 0.0112, 0.009786, 0.012539, 0.018116, 0.0211217, 0.1256712, 0.3290593, 0.5239033, 0.6069637, 0.8290751, 1.3396434, 2.59858862101087]})

# определяем DataFrame Африка
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [0.0063, 0.0071, 0.0072, 0.0076, 0.0198, 0.1755, 0.41558, 0.443584, 0.535599, 0.768280505050505, 0.780382111111111, 0.852565606060606, 1.01622336363934, 1.31177813131313, 1.58923093939543, 2.28458243433914, 2.38650393937963, 2.51563024049708, 3.59344730255575, 5.06007283421232, 8.91068628262324, 11.1763706727939, 12.4577740957429, 14.770723351763, 18.8577291329819, 21.7898430685021]})

# определяем DataFrame Asia Pacific
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [1.12160131313131, 0.991205066484849, 1.21395004149495, 1.48955016659596, 2.05324900639394, 2.56394697970469, 3.51740941797741, 4.06701324667883, 5.34087585515362, 9.18669339997316, 12.019193605714, 18.5698071338417, 24.6031314143647, 36.0798945954192, 54.8479782750866, 81.4841965496602, 113.551087628561, 147.723580093628, 188.472143425882, 214.272687090449, 243.060053246854, 311.20761354133, 387.097778226688, 461.951758065283, 509.368307094495, 572.636106061397]})

# определяем DataFrame Middle East
# data = pd.DataFrame({'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
#                      'generate': [0.001, 0.001, 0.003, 0.003, 0.038, 0.0395, 0.0467, 0.0443, 0.0426, 0.0614, 0.086, 0.1394, 0.155, 0.2101, 0.2405, 0.2222, 0.2258, 0.2166, 0.228089, 0.217278, 0.381789, 0.678, 0.795329, 1.33765, 1.55208140494423, 1.90417927964862]})
data['cum_sum'] = data['generate'].cumsum()
data['Sales'] = [0]+[data['generate'][i+1]-data['generate'][i] for i in range(data.shape[0]-1)]

finalYear = 2025  # Финальный год

def Bass(x, P, Q, M):
    """
    Функция расчета Prognose Sales
    x: величина Prognose Cumulative за прошлый год.
    """
    return (P*M+(Q-P)*(x))-(Q/M)*(x**2)

# Начальные значения параметров
# bounds = ([0, 0, 0], [np.inf, np.inf, np.inf])
popt, pcov = curve_fit(Bass, data.generate, data.Sales, bounds=(0, np.inf), method='trf', maxfev = 10000)
p0 = popt[0]
q0 = popt[1]
m0 = popt[2]
# p0 = 0.0000012
# q0 = 0.318
# m0 = 12

# Выводим стартовые коэффициенты
print('Стартовые коэффициенты:')
print('P0 =', p0)
print('Q0 =', q0)
print('M0 =', m0)

def squareMistake(k: tuple, *sales) -> float:
    """
    Функция для минимизации через scipy.
    Рассчитывает сумму квадратов разностей значений
    Prognose Cumulative и Prognose Sales.
    k: кортеж начальных параметров (P, Q, M);
    sales: кортеж Sales.
    """
    # Начальные значения для первого года
    p0 = 0  # Prognose Sales
    c0 = sales[0]  # Prognose Cumulative
    res = 0  # Значение функции
    # Набираем результат функции за годы
    for i in range(1, len(sales)):
        p = Bass(c0, P=k[0], Q=k[1], M=k[2])  # Новый Prognose Sales
        c = c0 + p  # Новый Prognose Cumulative
        res += (c - sales[i])**2  # Добавляем
        # Обновляем значения
        p0 = p
        c0 = c
    return res


# Формируем данные по годам
years1 = tuple(data.year)
gens = tuple(data.generate)

# Готовим данные для минимизации
k0 = [p0, q0, m0]  # Начальные значения параметров
kb = ((0, None), (0, None), (0, None))  # Все параметры неотрицательные

# Минимизируем сумму квадратов
res = minimize(squareMistake, k0, args=gens, method='Nelder-Mead', bounds=kb)

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
    prSales.append(Bass(prCumul[-1], P=k[0], Q=k[1], M=k[2]))  # Prognose Sales
    prCumul.append(prCumul[-1]+prSales[-1])  # Prognose Cumulative

# Формируем структуру выходных данных
dataOut = {}
dataOut['param'] = {'P': k[0], 'Q': k[1], 'M': k[2]}  # Параметры
dataOut['year'] = years2  # Года
dataOut['prSales'] = prSales  # Значения Prognose Sales
dataOut['prCumul'] = prCumul  # Значения Prognose Cumulative

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

# метрика суммы квадратов остатков (Residual Sum of Squares, RSS). Чем меньше значение RSS, тем лучше кривая описывает данные
def rss(y_real, y_predicted):
    """Результат должен быть близким к нулю, так как формула должна точно описывать логарифмическую кривую.
    Args:
        y_real (_type_): список или массив с реальными значениями, полученными из данных
        y_predicted (_type_): список или массив с предсказанными значениями на основе формулы.

    Returns:
        _type_: _description_
    """
    squared_residuals = np.square(np.subtract(y_real, y_predicted))
    return sum(squared_residuals)

# sales = np.array([data['Sales']])
# pr_Sales = np.array([i for i in prSales])
# print(len(gens))
# print(len(prCumul[:26]))
data['prCumul'] = prCumul[:len(gens)]
# y = Bass(gens, P, Q, M)
y_real = data['generate']
y_predicted = data['prCumul']
print(f"Сумма квадратов остатков - {rss(y_real, y_predicted)}")
# print(data)