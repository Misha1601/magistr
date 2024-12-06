import pandas as pd

# Пример 1: Простое объединение по индексу
df1 = pd.DataFrame({
    'A': ['A0', 'A1', 'A2'],
    'B': ['B0', 'B1', 'B2']
})

df2 = pd.DataFrame({
    'A': ['C0', 'C1', 'C2'],
    'D': ['D0', 'D1', 'D2']
})

# Вертикальное объединение (добавление строк)
result = pd.concat([df1, df2], axis=0)
print(result)


