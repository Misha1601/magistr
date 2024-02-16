import numpy
import matplotlib.pyplot as plt

hjroot = []

class HookeJeeves:
    @staticmethod
    def __exploring_search(basis_point: numpy.ndarray, step: numpy.ndarray, target_function) -> numpy.ndarray:
        """
        Исследующий поиск.
        Поиск точек по каждой оси вокруг базисной точки.
        Возвращает точку с минимальным значением целевой функции.
        """
        for i in step:
            if target_function(basis_point + i) < target_function(basis_point):
                basis_point = basis_point + i
            elif target_function(basis_point - i) < target_function(basis_point):
                basis_point = basis_point - i
        return basis_point

    @staticmethod
    def __pattern_search(basis_point, minimum, target_function, alpha: float) -> numpy.ndarray:
        """
        Поиск по образцу, пока целевая функция уменьшается.
        Возвращает точку с минимально возможным значением целевой функции.
        """
        d = (minimum - basis_point) * alpha
        next_point = minimum + d
        while target_function(next_point) < target_function(minimum):
            next_point, minimum = next_point + d, next_point
        return minimum

    @staticmethod
    def __stop_criteria(delta_x: numpy.ndarray, epsilon: float) -> bool:
        """
        Критерий останова.
        True когда длина каждого шага (по каждой оси) стала меньше epsilon
        """
        for i in delta_x:
            if numpy.linalg.norm(i) > epsilon:
                return False
        return True

    @staticmethod
    def optimization(basis_point: numpy.ndarray, delta_x: numpy.ndarray, target_function, alpha: float,
                     epsilon: float, decrement_parameter: float):
        """
        Главная функция оптимизации.
        Возвращает координаты точки и значение целевой функции в этой точке.
        """

        while not HookeJeeves.__stop_criteria(delta_x, epsilon):
            minimum = HookeJeeves.__exploring_search(basis_point, delta_x, target_function)
            # print(f"minimum= {minimum}\ntarget_function(minimum) = {target_function(minimum)}")
            # print(f"basis_point {basis_point}\ntarget_function(basis_point) = {target_function(basis_point)}")
            if numpy.array_equal(minimum, basis_point):
                delta_x *= decrement_parameter
                continue
            # Добавление точки в список точек (путь) (для графиков)
            hjroot.append(minimum)
            temp_basis_point = HookeJeeves.__pattern_search(basis_point, minimum, target_function, alpha)
            if numpy.array_equal(temp_basis_point, basis_point):
                delta_x *= decrement_parameter
                continue
            # Добавление точки в список точек (путь) (для графиков)
            hjroot.append(temp_basis_point)
            basis_point = temp_basis_point
        return basis_point, target_function(basis_point)


def function(point: numpy.ndarray) -> float:
    """Целевая функция"""
    # 0 at (4, -4)
    # return (point[0] - 4) ** 2 + (point[1] + 4) ** 2

    # 0 at (3, -3)
    # return (point[0] - 1) ** 2 + (point[1] + 1) ** 2

    # 0 at (1, 1)
    return 100 * (point[0] ** 2 - point[1]) ** 2 + (point[0] - 1) ** 2

    # 10.4265 at (0.731404, -0.365702)
    # return (point[0] + point[1]) ** 2 + (numpy.sin(point[0] + 2)) ** 2 + point[1] ** 2 + 10

    # 0 at (4, 2)
    # return (4 - point[0]) ** 2 + (2 - point[1]) ** 2


if __name__ == "__main__":
    """Графики"""
    x = numpy.arange(-20, 20, 0.5)
    y = numpy.arange(-20, 20, 0.5)
    X, Y = numpy.meshgrid(x, y)
    plt.contourf(X, Y, function(numpy.array([X, Y])), cmap='Reds', levels=20, alpha=1)

    """Метод Хука-Дживса"""
    # Приращения по каждой оси
    deltax = numpy.array([[1., 0.], [0., 1.]])
    # Начальная точка
    x0 = numpy.array([5., 12.])
    # alpha - коэффициент шага в поиске по образцу
    # epsilon - точность
    result = HookeJeeves.optimization(basis_point=x0, delta_x=deltax, target_function=function,
                                      alpha=1, epsilon=0.00001, decrement_parameter=0.5)
    print(f"Метод Хука-Дживса\t{result}")

    # метод Хука-Дживса отрисовка точек
    plt.scatter(x0[0], x0[1], color='blue', s=5)
    plt.plot([i[0] for i in hjroot], [i[1] for i in hjroot], color='black')
    plt.show()