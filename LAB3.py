import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.interpolate import interp1d


def cubic_interp1d(x0, x, y):
    x = np.asfarray(x)
    y = np.asfarray(y)
    size = len(x)

    xdiff = np.diff(x)
    ydiff = np.diff(y)

    Li = np.empty(size)
    Li_1 = np.empty(size - 1)
    z = np.empty(size)
    Li[0] = sqrt(2 * xdiff[0])
    Li_1[0] = 0.0
    B0 = 0.0
    z[0] = B0 / Li[0]

    for i in range(1, size - 1, 1):
        Li_1[i] = xdiff[i - 1] / Li[i - 1]
        Li[i] = sqrt(2 * (xdiff[i - 1] + xdiff[i]) - Li_1[i - 1] * Li_1[i - 1])
        Bi = 6 * (ydiff[i] / xdiff[i] - ydiff[i - 1] / xdiff[i - 1])
        z[i] = (Bi - Li_1[i - 1] * z[i - 1]) / Li[i]

    i = size - 1
    Li_1[i - 1] = xdiff[-1] / Li[i - 1]
    Li[i] = sqrt(2 * xdiff[-1] - Li_1[i - 1] * Li_1[i - 1])
    Bi = 0.0
    z[i] = (Bi - Li_1[i - 1] * z[i - 1]) / Li[i]

    i = size - 1
    z[i] = z[i] / Li[i]
    for i in range(size - 2, -1, -1):
        z[i] = (z[i] - Li_1[i - 1] * z[i + 1]) / Li[i]

    index = x.searchsorted(x0)
    np.clip(index, 1, size - 1, index)

    xi1, xi0 = x[index], x[index - 1]
    yi1, yi0 = y[index], y[index - 1]
    zi1, zi0 = z[index], z[index - 1]
    hi1 = xi1 - xi0

    f0 = zi0 / (6 * hi1) * (xi1 - x0) ** 3 + \
         zi1 / (6 * hi1) * (x0 - xi0) ** 3 + \
         (yi1 / hi1 - zi1 * hi1 / 6) * (x0 - xi0) + \
         (yi0 / hi1 - zi0 * hi1 / 6) * (xi1 - x0)
    return f0


x = [float(num) for num in open("input.txt").readline().split(' ')]
x.sort()
print("Введите номер выбраной функции")
token = int(input("1 : cos(x)\n" + "2 : x^2\n" + "3 : exp(x)\n"))
if token == 1:
    y = np.cos(x)
    func = np.cos
elif token == 2:
    y = np.square(x)
    func = np.square
elif token == 3:
    y = np.exp(x)
    func = np.exp
else:
    y = np.abs(x)
    func = np.abs

x_new = np.linspace(x[0], x[len(x) - 1], num=200)
new_points = cubic_interp1d(x_new, x, y)
f = interp1d(x, y, kind='cubic')
plt.plot(x, y, 'o', x_new, f(x_new), '-', x_new, func(x_new), '--')
plt.scatter(x, y)
plt.legend(['Данные', 'Кубическая', 'Реальная'], loc='best')
plt.grid()
plt.show()

try:
    while True:
        print(f([float(input("Введите х\n"))]))
except ValueError:
    print("Введенное число выходит за промежуток интерполяции")
