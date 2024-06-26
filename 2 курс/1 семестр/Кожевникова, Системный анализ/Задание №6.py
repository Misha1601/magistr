# Задание №6. Методом целочисленного программирования решить задачу:
# В цехе предприятия решено установить дополнительное оборудование, для размещения которого выделено 6 м2 площади. На приобретение оборудования предприятие может израсходовать 10 тыс. руб., при этом оно может купить оборудование двух видов. Комплект оборудования I вида стоит 1000 руб., а II вида – 3000 руб. Приобретение одного комплекта оборудования I вида позволяет увеличить выпуск продукции в смену на 2 ед., а одного комплекта оборудования II вида – на 4 ед. Зная, что для установки одного комплекта оборудования I вида требуется 2 м2 площади, а оборудования II вида – 1 м2 площади определить такой набор дополнительного оборудования, которых дает возможность максимально увеличить выпуск продукции.

from pulp import LpMaximize, LpProblem, LpVariable

# Создаем задачу на максимизацию
model = LpProblem(name="equipment_maximization", sense=LpMaximize)

# Определяем переменные
x = LpVariable(name="x", lowBound=0, cat="Integer")  # Количество оборудования I вида
y = LpVariable(name="y", lowBound=0, cat="Integer")  # Количество оборудования II вида

# Определяем целевую функцию для максимизации
model += 2 * x + 4 * y

# Добавляем ограничения
model += 2 * x + y <= 6  # Ограничение площади
model += 1000 * x + 3000 * y <= 10000  # Ограничение бюджета

# Решаем задачу
model.solve()

# Получаем оптимальные значения
x_optimal = x.varValue
y_optimal = y.varValue
max_Z = 2 * x_optimal + 4 * y_optimal

# Выводим результаты
print("Оптимальное количество оборудования I вида (x):", x_optimal)
print("Оптимальное количество оборудования II вида (y):", y_optimal)
print("Максимальное значение целевой функции (Z):", max_Z)
