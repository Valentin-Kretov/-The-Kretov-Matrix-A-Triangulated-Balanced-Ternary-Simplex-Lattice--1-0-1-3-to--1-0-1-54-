"""
The Kretov Matrix: 54D Cosmological & Holographic Emergence Engine (3^54 Scale)
Author: Valentin Aleksandrovich Kretov (Кретов Валентин Александрович)
File: kretov_54d_cosmology.py

Description:
    1. Exact polynomial convolution audit of the 54-dimensional simplex Omega_54 = {-1, 0, +1}^54,
       where 54 dimensions correspond to the 54 internal tensegrity edges of Omega_3.
    2. Verifies the Avogadro-scale state volume (3^54 ~ 5.815e25), exact zero-balance count
       (3.853e24 states, 6.63% equilibrium share), and exact integer dispersion sigma = 6.0000.
    3. Simulates Micro-Stability vs. Macro-Evolution under Gaussian noise (sigma = 0.35):
       89.79% individual axis preservation vs. 99.71% holistic 54D state evolution.
    4. Generates a publication-grade plot comparing quantum discrete states (3^3) vs.
       emergent classical Gaussian continuity (3^54) saved as 'kretov_54d_emergence.png'.
"""

import numpy as np
import matplotlib.pyplot as plt

def exact_polynomial_audit_54d():
    """Точный комбинаторный расчет пространства 3^54 через свертку триномиальных коэффициентов."""
    print("=" * 88)
    print("1. ТОЧНЫЙ КОМБИНАТОРНЫЙ АУДИТ КОСМОЛОГИЧЕСКОГО ПРЕДЕЛА (3^6)^9 = 3^54")
    print("=" * 88)

    dim_54 = 54  # Равно 54 внутренним ребрам базовой Матрицы Кретова Omega_3
    total_states = 3 ** dim_54
    total_edges_54 = 2 * dim_54 * (3 ** (dim_54 - 1))

    # Точное вычисление распределения зарядов Q от -54 до +54 через 54-кратную свертку (1 + x + x^2)
    kernel = np.ones(3, dtype=object)
    poly = np.ones(1, dtype=object)
    for _ in range(dim_54):
        poly = np.convolve(poly, kernel)

    zero_balance_states = poly[dim_54]
    equilibrium_share = (float(zero_balance_states) / float(total_states)) * 100.0
    exact_sigma = np.sqrt(2.0 * dim_54 / 3.0)

    print(f"  Размерность гиперрешетки:             {dim_54}D (54 ребра базового симплекса Omega_3)")
    print(f"  Полный объем состояний (3^54):        {float(total_states):.4e} (масштаб числа Авогадро)")
    print(f"  Число связей тенсегрити в 54D:       {float(total_edges_54):.4e}")
    print(f"  Состояния равновесия (Q = 0):         {float(zero_balance_states):.4e}")
    print(f"  Доля нулевого баланса:                {equilibrium_share:.2f}% (точное значение: 6.63%)")
    print(f"  Теоретическая дисперсия заряда:       sigma = {exact_sigma:.4f} (точное целое число 6)")
    print(f"  Вероятность абсолютного покоя (0^54): {3.0**(-dim_54):.4e} (рождение макро-инерции)\n")

    return poly

def simulate_54d_emergence_and_evolution(n_trials: int = 1_000_000, noise_sigma: float = 0.35, seed: int = 42):
    """Монте-Карло моделирование классического предела Гаусса и эволюционной динамики в 54D."""
    print("=" * 88)
    print(f"2. МОНТЕ-КАРЛО СИМУЛЯЦИЯ ЭМЕРДЖЕНТНОСТИ В 54D (N = {n_trials:,} ИСПЫТАНИЙ)")
    print("=" * 88)

    rng = np.random.default_rng(seed)
    dim_54 = 54
    alphabet = np.array([-1, 0, 1], dtype=np.int8)

    # Генерация 1 000 000 случайных конфигураций в 54-мерном пространстве
    states = rng.choice(alphabet, size=(n_trials, dim_54))
    charges = np.sum(states, axis=1, dtype=np.int32)

    mean_q = np.mean(charges)
    std_q = np.std(charges)
    zero_q_pct = np.mean(charges == 0) * 100.0

    # Проверка закона «Микро-стабильность против Макро-эволюции»
    noisy_states = states + rng.normal(0.0, noise_sigma, size=(n_trials, dim_54))
    recovered_states = np.clip(np.round(noisy_states), -1, 1).astype(np.int8)

    micro_axis_stability = np.mean(states == recovered_states) * 100.0
    macro_vector_unchanged = np.mean(np.all(states == recovered_states, axis=1)) * 100.0
    macro_evolution_rate = 100.0 - macro_vector_unchanged

    print(f"  [Классический предел Гаусса]")
    print(f"    Средний топологический заряд:       {mean_q:+.5f} (теория: 0.00000)")
    print(f"    Измеренная дисперсия (sigma):       {std_q:.4f} (теория: 6.0000)")
    print(f"    Доля состояний с Q = 0:             {zero_q_pct:.2f}% (теория: 6.63%)")
    print(f"\n  [Закон микро-стабильности и макро-эволюции при шуме sigma = {noise_sigma}]")
    print(f"    Стабильность отдельного узла (атома):     {micro_axis_stability:.2f}% (сохранение структуры)")
    print(f"    Неизменность всего 54D-вектора целиком:   {macro_vector_unchanged:.2f}%")
    print(f"    Частота обновления 54D-системы (эволюция): {macro_evolution_rate:.2f}% (непрерывное развитие)\n")

    return charges

def plot_quantum_to_classical_transition(charges_54d):
    """Визуализация перехода от дискретной решетки 3^3 к непрерывному гауссиану 3^54."""
    print("=" * 88)
    print("3. ПОСТРОЕНИЕ ГРАФИКА КВАНТОВО-КЛАССИЧЕСКОГО ПЕРЕХОДА ('kretov_54d_emergence.png')")
    print("=" * 88)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), facecolor="#0b0f19")

    # Левая панель: Дискретная пирамида базовой Матрицы Кретова (3^3 = 27)
    ax1 = axes[0]
    ax1.set_facecolor("#111827")
    q_3d = np.array([-3, -2, -1, 0, 1, 2, 3])
    counts_3d = np.array([1, 3, 6, 7, 6, 3, 1]) / 27.0 * 100.0
    colors_3d = ["#3b82f6", "#60a5fa", "#93c5fd", "#fbbf24", "#fca5a5", "#f87171", "#ef4444"]

    ax1.bar(q_3d, counts_3d, color=colors_3d, edgecolor="white", linewidth=1.0, width=0.6)
    ax1.set_title("Quantum Scale: Base Matrix 3³ = 27\n(Discrete 1-3-6-7-6-3-1 Spectrum)", color="white", fontsize=11.5, pad=12)
    ax1.set_xlabel("Topological Charge Q = x + y + z", color="white", fontsize=10)
    ax1.set_ylabel("Probability Density (%)", color="white", fontsize=10)
    ax1.tick_params(colors="white")
    ax1.grid(axis="y", linestyle="--", alpha=0.2, color="white")

    # Правая панель: Эмерджентный классический гауссиан 3^54 (sigma = 6.0000)
    ax2 = axes[1]
    ax2.set_facecolor("#111827")
    bins = np.arange(-25.5, 26.5, 1.0)
    ax2.hist(charges_54d, bins=bins, density=True, color="#38bdf8", alpha=0.75, edgecolor="#0f172a", label="Monte Carlo 3⁵⁴ (10⁶ trials)")

    # Теоретическая кривая нормального распределения с целой дисперсией sigma = 6.0
    x_grid = np.linspace(-25, 25, 400)
    sigma = 6.0
    gaussian_pdf = (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * (x_grid / sigma) ** 2)
    ax2.plot(x_grid, gaussian_pdf, color="#fbbf24", linewidth=2.5, label="Exact Gaussian Limit (σ = 6.0000)")

    ax2.set_title("Macroscopic Limit: Holographic Lattice 3⁵⁴\n(Emergent Classical Gaussian Continuum)", color="white", fontsize=11.5, pad=12)
    ax2.set_xlabel("Net Macroscopic Charge Q (54 Edges)", color="white", fontsize=10)
    ax2.set_ylabel("Probability Density", color="white", fontsize=10)
    ax2.tick_params(colors="white")
    ax2.grid(linestyle="--", alpha=0.2, color="white")
    ax2.legend(loc="upper right", facecolor="#1f2937", edgecolor="gray", labelcolor="white", fontsize=9)

    plt.tight_layout()
    plt.savefig("kretov_54d_emergence.png", dpi=300, facecolor=fig.get_facecolor())
    print("Готово! График квантово-классического перехода сохранен в 'kretov_54d_emergence.png'.")

if __name__ == "__main__":
    exact_polynomial_audit_54d()
    charges = simulate_54d_emergence_and_evolution(n_trials=1_000_000, noise_sigma=0.35, seed=42)
    plot_quantum_to_classical_transition(charges)
