import numpy as np
from scipy.integrate import simpson

def qua_mech_ave_p(Psi, X):
    """Вычисление квантовомеханического среднего <p>"""
    # hbar = 1 в атомных единицах, или hbar = 1.0545718e-34 в СИ
    hbar = 1.0  # для простоты, можно изменить
    
    # Вычисляем производную волновой функции
    dPsi_dx = np.gradient(Psi, X)
    
    # Вычисляем числитель: ∫ ψ* (-iħ dψ/dx) dx
    # Для комплексных функций нужно комплексное сопряжение
    if np.iscomplexobj(Psi):
        num = simpson(np.conj(Psi) * (-1j * hbar * dPsi_dx), X)
        norm = simpson(np.abs(Psi)**2, X)
    else:
        # Для вещественных функций
        num = simpson(Psi * (-1j * hbar * dPsi_dx), X)
        norm = simpson(Psi**2, X)
    
    # Мнимая часть должна быть малой (проверка)
    result = num / norm if abs(norm) > 1e-12 else 0
    return result

def qua_mech_ave_p2(Psi, X):
    """Вычисление квантовомеханического среднего <p^2>"""
    hbar = 1.0
    
    # Вычисляем вторую производную
    dPsi_dx = np.gradient(Psi, X)
    d2Psi_dx2 = np.gradient(dPsi_dx, X)
    
    # Вычисляем числитель: ∫ ψ* (-ħ² d²ψ/dx²) dx
    if np.iscomplexobj(Psi):
        num = simpson(np.conj(Psi) * (-hbar**2 * d2Psi_dx2), X)
        norm = simpson(np.abs(Psi)**2, X)
    else:
        num = simpson(Psi * (-hbar**2 * d2Psi_dx2), X)
        norm = simpson(Psi**2, X)
    
    # Результат должен быть вещественным
    result = num / norm if abs(norm) > 1e-12 else 0
    return np.real(result)  # Берем вещественную часть
