"""
Вычисление собственных значений и собственных функций
оператора Гамилтона методом пристрелки.
Одномерная потенциальная яма с бесконечными стенками.
Атомные единицы Хартри.
Версия 2.
"""

import numpy as np
from scipy.integrate import odeint
# from scipy.misc import derivative
from scipy.optimize import approx_fprime
from scipy.interpolate import interp1d
from scipy.integrate import simpson

from qma import qua_mech_ave_p, qua_mech_ave_p2
import matplotlib.pyplot as plt
global r, n, Psi, Fi, X, XX
plt.rcParams['figure.figsize'] = [8, 6]

LST = open("schrodinger-2b.txt", "wt")

# потенциальная функция, рис. 3
# (на рис.3. "а" соответствует "L")
def U(x):
    # return float(U0 if abs(x) < L else W)
    if (x > -L) and (x < L):
        y = (-1 + (x + L) / (2 * L))
    else:
        y = 9999999
    return y

# функция, ф-ла (13)
def q(e, x):
    return 2.0*(e-U(x))

# вычисление правых частей системы ОДУ 1-го порядка
# (интегрирование "вперёд")
def system1(cond1, X):
    global eee
    Y0, Y1 = cond1[0], cond1[1]
    dY0dX = Y1
    dY1dX = - q(eee, X)*Y0
    return [dY0dX, dY1dX]


# вычисление правых частей системы ОДУ 1-го порядка
# (интегрирование "назад")
def system2(cond2, X):
    global eee
    Z0, Z1 = cond2[0], cond2[1]
    dZ0dX = Z1
    dZ1dX = - q(eee, X)*Z0
    return [dZ0dX, dZ1dX]

# вычисление разности производных в узле сшивки,
# формула (18)
def f_fun(e):
    global r, n, Psi, Fi, X, XX, eee
    eee = e
    """
    Решение задачи Коши ("Вперёд")
    Psi1(x)/dx = - q(e, x) * Psi(x);
    dPsi(x)/dx = Psi1(x);
    Psi(A) = 0.0
    Psi1(A) = 1.0
    """
    cond1 = [0.0, 1.0]
    sol1 = odeint(system1, cond1, X)
    Psi, Psi1 = sol1[:, 0], sol1[:, 1]
    """
    Решение задачи Коши ("назад")
    Psi1(x)/dx = - q(e, x) * Psi(x);
    dPsi(x)/dx = Psi1(x);
    Psi(B) = 0.0
    Psi1(B) = 1.0
    """
    cond2 = [0.0, 1.0]
    sol2 = odeint(system2, cond2, XX)
    Fi, Fi1 = sol2[:, 0], sol2[:, 1]
    # поиск максимального по величине элемента Psi
    p1 = np.abs(Psi).max()
    p2 = np.abs(Psi).min()
    big = p1 if p1 > p2 else p2
    # масштабирование Psi
    Psi[:] = Psi[:]/big
    # математическая нормировка Fi для
    # достижения равенства F[rr]=Psi[r]
    coef = Psi[r]/Fi[rr]
    Fi[:]=coef*Fi[:]
    # вычисление f(E) для узла сшивки, формула(18)
    curve1 =interp1d(X, Psi, kind='cubic')
    curve2 =interp1d(XX, Fi, kind='cubic')
    # der1 = derivative(curve1, X[r], dx=1.e-6)
    der1 = approx_fprime(X[r], curve1, epsilon=1.e-6)
    # der2 = derivative(curve1, XX[rr], dx=1.e-6)
    der2 = approx_fprime(XX[rr], curve2, epsilon=1.e-6)
    # print(f"debugprint: 1 {der1} -- 2 {der2}")
    f=der1[0]-der2[0]
    return f

#функция для решения уравнения f(E) = 0 методом бисекций
def m_bis(x1, x2, tol):
    global r, n
    # Проверка наличия корня на интервале
    if f_fun(e=x2) * f_fun(e=x1) > 0.0:
        print("ERROR::no_root!!!")
        print("x1 =", x1)
        print("x2 =", x2)
        print("f_fun(x1) =", f_fun(e=x1))
        print("f_fun(x2) =", f_fun(e=x2))
        exit()
    # Итерационный процесс метода бисекции
    while abs(x2 - x1) > tol:
        xr = (x1 + x2) / 2.0
        if f_fun(e=x2) * f_fun(e=xr) < 0.0:
            x1 = xr
        else:
            x2 = xr
        if f_fun(e=x1) * f_fun(e=xr) < 0.0:
            x2 = xr
        else:
            x1 = xr
    # Возвращаем приближенное значение корня
    return (x1 + x2) / 2.0

# Функция для вывода графика волновых функций и потенциала
def plotting_wf(e):
    global r, n, Psi, Fi, X, XX
    A_edge = A - 0.1 # расширяем слева
    B_edge = B + 0.1  # расширяем справа
    ff = f_fun(e)
    # Установка границ графика
    plt.axis([A_edge, B_edge, -1, W])
    # Вычисление потенциала
    Upot = np.array([U(X[i]) for i in np.arange(n)])
    # Построение графика потенциала
    plt.plot(X, Upot, 'g-', linewidth=6.0, label="U(x)")
    # Нулевая линия
    Zero = np.zeros(n, dtype=float)
    plt.plot(X, Zero, 'k-', linewidth=1.0)
    # Волновые функции
    plt.plot(X, Psi, 'r-', linewidth=5.0, label="Psi(x)")

    plt.plot([X[r]], [Psi[r]], color = 'red', marker = 'o', markersize = 8)
    plt.plot(X, prob_density, 'm--', linewidth = 2.0, label = "|Psi(x)|^2")

    plt.plot(XX, Fi, 'b-', linewidth=2.0, label="Fi(x)")

    # Настройка осей
    plt.xlabel("X", fontsize=18, color="k")
    plt.ylabel("Psi(x), Fi(x), U(X)", fontsize=18, color="k")
    plt.grid(True)
    # Легенда
    plt.legend(fontsize=16, shadow=True, fancybox=True, loc='upper right')
    # Отметка специальной точки
    plt.plot([X[r]], [Psi[r]], color='red', marker='o', markersize=7)
    # Текст с информацией об энергии и функции
    string1 = "E = " + format(e, "10.7f")
    string2 = "f(E) = " + format(ff, "10.3e")
    plt.text(-1.5, 2.7, string1, fontsize=14, color='black')
    plt.text(-1.5, 2.3, string2, fontsize=14, color="black")
    # Сохранение в файл
    name = "schrodinger-2b-" + str(ngr) + ".pdf"
    plt.savefig(name, dpi=300)
    plt.show()

# Задание отрезка [A, B] (края ямы)
# L = 2.0
L = 3.5
A = -L
B = +L

# Кол-во узлов сетки на [A, B]
n = 1001  # нечетное целое число
print("n =", n)
print("n =", n, file=LST)

# Минимальное значение потенциальной функции
U0 = -1.0

# Максимальное значение потенциальной функции на графике
W = 4.0

# x-координаты узлов сетки
X = np.linspace(A, B, n)   # для интегрирования "спереди"
XX = np.linspace(B, A, n)  # для интегрирования "назад"

# Номер узла сетки
r = (n - 1) * 3 // 4  # для Psi
rr = n - r - 1        # для Fi

print("r =", r)
print("r =", r, file=LST)
print("rr =", rr)
print("rr =", rr, file=LST)
print("X[r] =", X[r])
print("X[r] =", X[r], file=LST)
print("XX[rr] =", XX[rr])
print("XX[rr] =", XX[rr], file=LST)
# Поиск корней f(E)
e1 = U0 + 0.05
e2 = 3.0
print("e1 =", e1, "   e2 =", e2)
print("e1 =", e1, "   e2 =", e2, file=LST)

ne = 201
print("ne =", ne)
print("ne =", ne, file=LST)

prob_density = np.zeros(n)

ee = np.linspace(e1, e2, ne)
af = np.zeros(ne, dtype=float)
porog = 5.0
tol = 1.0e-7
energy = []
ngr = 0

qma_p_l = []
qma_pp_l = []
# Цикл поиска корней f(E) на отрезке [e1, e2]
for i in np.arange(ne):
    e = ee[i]
    af[i] = f_fun(e)

    stroka = "i = {:3d}   e = {:8.5f}   f(e) = {:12.5e}"
    print(stroka.format(i, e, af[i]))
    print(stroka.format(i, e, af[i]), file=LST)

    if i > 0:
        Log1 = af[i] * af[i-1] < 0.0  # проверка смены знака
        Log2 = np.abs(af[i] - af[i-1]) < porog  # проверка непрерывности

        if Log1 and Log2:
            energy1 = ee[i-1]
            energy2 = ee[i]
            eval = m_bis(energy1, energy2, tol)  # уточнение корня методом бисекции

            print("eval = {:12.5e}".format(eval))

            # Построение графика волновой функции
            energy.append(eval)

            norm_factor = simpson(Psi**2, X)
            if norm_factor != 0:
                Psi[:] = Psi / np.sqrt(norm_factor)
            prob_density = Psi**2

            dummy = plotting_wf(eval)

            Psi_copy = Psi.copy()
            p_qma = qua_mech_ave_p(Psi_copy, X)
            pp_qma = qua_mech_ave_p2(Psi_copy, X)

            qma_p_l.append(p_qma)
            qma_pp_l.append(pp_qma)

            ngr += 1

# Вывод значений корней уравнения f(E) = 0
print(qma_p_l)
tt = "----------------------------------"
print(tt)
print(tt, file = LST)
print("           ЭНЕРГИИ")
print("           ЭНЕРГИИ", file = LST)
print(tt)
print(tt, file = LST)
print("k       E, a.u.         E, eV")
print("k       E, a.u.         E, eV", file = LST)
print(tt)
print(tt, file = LST)
for k in range(ngr):
    print("{:1d}    {:12.7f}    {:12.7f}".format(k, energy[k], 27.211*energy[k]))
    print("{:1d}    {:12.7f}    {:12.7f}".format(k, energy[k], 27.211*energy[k]), file = LST)

print("  ")
print("  ", file = LST)
print("  ")
print("  ", file = LST)

print(tt)
print(tt, file = LST)
print("   КВАНТОВОМЕХАНИЧЕСКИЕ СРЕДНИЕ")
print("   КВАНТОВОМЕХАНИЧЕСКИЕ СРЕДНИЕ", file = LST)
print(tt)
print(tt, file = LST)
print("k       <x>             <x^2>")
print("k       <x>             <x^2>", file= LST)
print(tt)
print(tt, file = LST)
for k in range(ngr):
    print("{:1d}    {:12.7f}    {:12.7f}".format(k, qma_p_l[k], qma_pp_l[k]))
    print("{:1d}    {:12.7f}    {:12.7f}".format(k, qma_p_l[k], qma_pp_l[k]), file = LST)

fmax = +10.0
fmin = -10.0