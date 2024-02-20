import numpy as np
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

# Разделим данные на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Стандартизируем данные (приведем к среднему = 0 и стандартному отклонению = 1)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Создаем нейронную сеть
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(4,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')
])

# Компилируем модель
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучаем модель на обучающем наборе
model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.1)

# Оцениваем производительность модели на тестовом наборе данных
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Точность на тестовом наборе данных: {test_accuracy:.4f}")

# Предположим, у вас есть новые данные для ириса, которые вы хотите классифицировать
new_data = np.array([[4.7, 3.4, 1.7, 0.2]])  # Пример новых данных

# Стандартизируем новые данные так же, как и обучающие данные
new_data = scaler.transform(new_data)

# Используем обученную модель для классификации новых данных
predictions = model.predict(new_data)

# Получим индекс класса с наибольшей вероятностью
predicted_class_index = np.argmax(predictions)

# Получим исходное название класса на основе индекса
iris_classes = ['Setosa', 'Versicolor', 'Virginica']
predicted_class = iris_classes[predicted_class_index]

print(f"Модель предсказывает, что это ирис: {predicted_class}")

