import pandas as pd

df = pd.DataFrame({'k1': [17.0, 25.0, 50, 60, 70]})
df = df.assign(k2=lambda x: x['k1'] * 9 / 5 + 32,
               k3=lambda x: (x['k2'] +  459.67) * 5 / 9)


# df = df.assign(g=lambda x: 3 + x['g'].shift(1, fill_value=0))

# df = df.assign(i1=df.k2 - df.k1).assign(i1=lambda x: x.i1 + x.i1.shift().fillna(0))
df = df.assign(i1=df.k2 - df.k1).assign(i1=lambda x: x.i1 + x.i1.shift(1, fill_value=0))
print(df)