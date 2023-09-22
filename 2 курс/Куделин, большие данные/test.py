# Импортируем необходимые библиотеки
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

# Загрузим датасет Ирисы Фишера
iris = datasets.load_iris()
X = iris.data
y = iris.target

# print(iris.DESCR)

# pd.set_option('max_columns', 5)
# pd.set_option('display.width', None)

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)

iris_df['species'] = [iris.target_names[i] for i in iris.target]

# pd.set_option('precision', 2)

# print(iris_df.describe())

sns.set(font_scale=1.1)
sns.set_style('whitegrid')
grid = sns.pairplot(data=iris_df, vars=iris_df.columns[0:4], hue='species')
grid.savefig('pairplots.pdf')
