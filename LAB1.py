import numpy as np
import random


def wrong_input():
    print("Неверное количество неизвестных!")


def determinant_zero():
    print('Детерминант равен 0, нахождение решения невозможно')


# Функция вывода матрицы
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("%2.4f" % (matrix[i][j]), end=' ')
        print()


# Генерация случайной матрицы
def random_matrix():
    try:
        n = int(input("Введите количество неизвестных(от 1 до 20): "))
    except ValueError:
        wrong_input()
        random_matrix()
    if n < 1 or n > 20:
        wrong_input()
        random_matrix()
    else:
        matrix = [[random.random() for e in range(n + 1)] for e in range(n)]
    return matrix


# Чтение матрицы из файла
def read_from_file():
    path = input("Укажите путь к файлу")
    try:
        f = open(path, "r")
        matrix = [[float(num.replace(",", ".")) for num in line.split(' ')] for line in f]
    except FileNotFoundError:
        print("Неверный путь")
        read_from_file()
    return matrix


# Чтение матрицы с клавиотуры
def read_from_keyboard():
    j = 0
    i = 0
    try:
        n = int(input("Введите количество неизвестных(от 1 до 20): "))
    except ValueError:
        wrong_input()
        read_from_keyboard()
    if n < 1 or n > 20:
        wrong_input()
        read_from_keyboard()
    else:
        matrix = np.zeros((n, n + 1))
        print("Введите коэффициенты при неизвестных и свободные члены по порядку в формате")
        print("a11 a12 a13 ... a1n b1")
        print("a21 a22 a23 ... a2n b2")
        print("и тд.")
        print("Ввод: ")
        while i < n:
            while j < (n + 1):
                try:
                    matrix[i][j] = float(input())
                    j += 1
                except ValueError:
                    print("Произошла ошибка ввода, пожалуйста, введите последний символ заново.")
            i += 1
            j = 0
    print_matrix(matrix)
    return matrix


# функция выбора главного элемента
def matrix_max(matrix, n):
    max_element = matrix[n][n]
    max_row = n
    for i in range(n + 1, len(matrix)):
        if abs(matrix[n][i]) > abs(max_element):
            max_element = matrix[n][i]
            max_row = i
        if max_row != n:
            matrix[n], matrix[max_row] = matrix[max_row], matrix[n]
    return matrix


# Реализация метода Гаусса
def gauss(matrix):
    square_matrix = matrix.copy()
    square_matrix = np.delete(square_matrix, len(matrix), 1)
    det = np.linalg.det(square_matrix)
    if det == 0:  # Проверка детерминанта
        determinant_zero()
        return

    n = len(matrix)
    for k in range(n - 1):
        matrix_max(matrix, k)
        for i in range(k + 1, n):
            div = matrix[i][k] / matrix[k][k]
            matrix[i][-1] -= div * matrix[k][-1]
            for j in range(k, n):
                matrix[i][j] -= div * matrix[k][j]
    for k in range(n - 1, -1, -1):
        x[k] = (matrix[k][-1] - sum([matrix[k][j] * x[j] for j in range(k + 1, n)])) / matrix[k][k]
    return x


# Подсчет и вывод невязки
def residual(matrix):
    temp = np.zeros((20, 1))
    r = np.zeros((20, 1))
    square_matrix = np.delete(matrix, len(matrix), 1)
    b = np.delete(matrix, np.s_[0:len(matrix)], 1)
    print('Вектор невязки:')
    for i in range(len(square_matrix)):
        temp[i] = 0
        for j in range(len(square_matrix)):
            temp[i] += x[j] * square_matrix[i][j]
        r[i] = temp[i] - b[i]
        print('r[', i + 1, '] =', "%.24f" % (r[i]), end='\n')


# Вывод треугольной матрицы, решения, определителя
def print_gauss_matrix(x, matrix):
    square_matrix = np.delete(matrix, len(matrix), 1)
    if np.linalg.det(square_matrix) == 0:
        return
    print(" ")
    print("Решение методом Гауса: ")
    for k in range(len(x)):
        if x[k] != 0:
            print('x[', k + 1, '] =', "%2.4f" % (x[k]), end='\n')
    print(" ")
    print('A:')
    print_matrix(matrix)
    square_matrix = np.delete(matrix, len(matrix), 1)
    print(" ")
    print("Определитель:", np.linalg.det(square_matrix))
    residual(matrix)
    return x


# Генерация массива для ответов
x = np.zeros((20, 1))
# UI
print("Программа для решения СЛАУ методом Гаусса с выбором главного элемента.")
while True:
    x = np.zeros((20, 1))
    token = input("Для начала работы введите" +
                  "\n 1 или k чтобы ввести матрицу с клавиатуры," +
                  "\n 2 или r для заполнения случайными значениями," +
                  "\n 3 или f для считывания из файла " +
                  "\n 4 или q для выхода из программы: ")
    if token == "1" or token == "k":
        matrix = read_from_keyboard()
        print_matrix(matrix)
        gauss(matrix)
        print_gauss_matrix(x, matrix)
    elif token == "2" or token == "r":
        matrix = random_matrix()
        print_matrix(matrix)
        gauss(matrix)
        print_gauss_matrix(x, matrix)
    elif token == "3" or token == "f":
        matrix = read_from_file()
        print_matrix(matrix)
        gauss(matrix)
        print_gauss_matrix(x, matrix)
    elif token == "4" or token == "q":
        print("q")
        exit(0)
    else:
        print("Неправильный ввод")
