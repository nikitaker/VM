import matplotlib.pyplot as plt
from math import sqrt, cos
import numpy as np
from scipy.interpolate import interp1d


def good_input(text):
    try:
        print()
        x = float(input("Введите " + str(text) + "\n"))
        if text == "точность" and x <= 0:
            print("точность должна быть больше 0")
            return good_input(text)
        return x
    except ValueError:
        print("Ввод неверен, повторите ввод снова")
        return good_input(text)


def runge_kutta(x, y, h, f):
    k_1 = h * f(x, y)
    k_2 = h * f(x + h / 2, y + k_1 / 2)
    k_3 = h * f(x + h / 2, y + k_2 / 2)
    k_4 = h * f(x + h, y + k_3)
    return y + k_1 / 6 + k_2 / 3 + k_3 / 3 + k_4 / 6


print("Введите номер выбраной функции")
token = int(input("1 : y*cos(x)\n" + "2 : x^2\n" + "3 : x-y\n"))
if token == 1:
    func = lambda x, y: y * cos(x)
elif token == 2:
    func = lambda x, y: x ** 2
elif token == 3:
    func = lambda x, y: x - y
else:
    exit("Введенный номер функции неверен")

x0 = good_input("x0")
y0 = good_input("y0")
xn = good_input("xn")
if x0 - xn == 0:
    exit("Начало и конец промежутка в одной точке")
accuracy = good_input("точность")
h = sqrt(sqrt(accuracy))
n = (xn - x0) / h
x_list = np.linspace(x0, xn, num=int(n))
y_list = []
y = y0
y_list.append(y)
for x in x_list[1:]:
    y = runge_kutta(x, y, h, func)
    y_list.append(round(y, 5))

f = interp1d(x_list, y_list, kind='cubic')
plt.plot(x_list, y_list, 'o', x_list, f(x_list), '-')
plt.scatter(x, y)
plt.legend(['Данные', 'Кубическая'], loc='best')
plt.grid()
plt.show()
