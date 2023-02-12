import pandas as pd
import numpy as np

df = pd.DataFrame({'k1': [17.0, 25.0, 50, 60, 70]})
df = df.assign(k2=lambda x: x['k1'] * 9 / 5 + 32,
               k3=lambda x: (x['k2'] +  459.67) * 5 / 9)


# df = df.assign(g=lambda x: 3 + x['g'].shift(1, fill_value=0))

# df = df.assign(i1=df.k2 - df.k1).assign(i1=lambda x: x.i1 + x.i1.shift().fillna(0))
df = df.assign(i1=df.k2 - df.k1).assign(i1=lambda x: x.i1 + x.i1.shift(1, fill_value=0))
# print(df)

# numbers = np.random.randint(1, 101, 10)
numbers = np.random.choice(np.arange(1, 101), 10, replace=False)
# print(numbers)
# print(sum(numbers))

def get_list_of_numbers(num1, num2):
    result = []
    diff = num2 - num1
    step = diff / 10
    for i in range(10):
        result.append(num1 + i * step)
    return result

def get_list_of_10_elements(num):
    result = []
    for i in range(20):
        result.append(num // (20 - i))
        num -= num // (20 - i)
    return result

a = get_list_of_10_elements(75)
print(a)
print(sum(a))
