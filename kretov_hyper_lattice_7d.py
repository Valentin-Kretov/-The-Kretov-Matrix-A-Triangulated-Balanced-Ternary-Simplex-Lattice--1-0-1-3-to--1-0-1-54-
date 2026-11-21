"""
The Kretov Matrix: 7D Hyper-Lattice Scaling Audit (3^0 -> 3^7) & Petrie Rosette Visualizer
Author: Valentin Aleksandrovich Kretov (Кретов Валентин Александрович)
File: kretov_hyper_lattice_7d.py

Description:
    1. Audits the fractal scaling hierarchy from n=0 (3^0 = 1) to n=7 (3^7 = 2,187 states),
       computing tensegrity edges (2n * 3^(n-1)), zero-balance attractors (Q = 0),
       equilibrium shares, and charge dispersion sigma = sqrt(2n/3).
    2. Analyzes micro-stability vs. macro-evolution resilience in 7D (2,187 nodes).
    3. Projects the 7-dimensional balanced ternary simplex onto a 2D Petrie polygon plane
       with 14-fold rotational symmetry ('kretov_7d_rosette.png').
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt

def run_7d_scaling_audit():
    """Аудит фрактальной лестницы от 3^0 до 3^7 (2 187 узлов)."""
    print("=" * 88)
    print("1. АУДИТ ФРАКТАЛЬНОЙ ЛЕСТНИЦЫ МАТРИЦЫ КРЕТОВА (3^0 -> 3^7)")
    print("=" * 88)

    correspondences = {
        0: "Сингулярность / Единое Поле",
        1: "Базовый треугольник {-1, 0, +1} (3 цвета / поколения)",
        2: "Триангулированный слой (8 глюонов + 1 фотон)",
        3: "Матрица Кретова (26 констант СМ + theta_QCD = 0)",
        4: "4D-симплекс материи (81 стабильный химический элемент)",
        5: "Ядерно-молекулярный предел (граница стабильности изотопов A ~ 243)",
        6: "Гармонический резонанс (27 x 27 = 729; 6D многообразие Калаби-Яу)",
        7: "14-лучевая розетка симметрии (сложные самоорганизующиеся сети)"
    }

    kernel = np.ones(3, dtype=int)
    for n in range(8):
        total_states = 3 ** n
        edges = 0 if n == 0 else 2 * n * (3 ** (n - 1))
        sigma = np.sqrt(2.0 * n / 3.0)

        # Точный подсчет состояний равновесия Q = 0 через свертку полинома (1 + x + x^2)^n
        if n == 0:
            zero_states = 1
        else:
            poly = np.ones(1, dtype=int)
            for _ in range(n):
                poly = np.convolve(poly, kernel)
            zero_states = poly[n]

        eq_share = (zero_states / total_states) * 100.0
        print(f"  3^{n} = {total_states:4d} узлов | Ребер: {edges:5d} | Q=0: {zero_states:3d} ({eq_share:6.2f}%) | "
              f"sigma={sigma:.4f} | {correspondences[n]}")
    print()

def test_7d_system_stability(n_trials: int = 500_000, sigma: float = 0.35, seed: int = 42):
    """Проверка устойчивости 7D-системы при непрерывном гауссовском шуме."""
    print("=" * 88)
    print(f"2. АНАЛИЗ УСТОЙЧИВОСТИ 7D-ГИПЕРРЕШЕТКИ (N = {n_trials:,}, ШУМ sigma = {sigma})")
    print("=" * 88)

    rng = np.random.default_rng(seed)
    dim = 7
    states = rng.choice([-1, 0, 1], size=(n_trials, dim))
    noisy = states + rng.normal(0.0, sigma, size=(n_trials, dim))
    recovered = np.clip(np.round(noisy), -1, 1).astype(int)

    axis_stability = np.mean(states == recovered) * 100.0
    vector_exact_recovery = np.mean(np.all(states == recovered, axis=1)) * 100.0
    vector_evolution_rate = 100.0 - vector_exact_recovery

    print(f"  Стабильность отдельной оси (сохранение базовых элементов): {axis_stability:.2f}%")
    print(f"  Полное сохранение 7D-вектора без изменений:                {vector_exact_recovery:.2f}%")
    print(f"  Частота адаптивного обновления 7D-системы (эволюция):      {vector_evolution_rate:.2f}%\n")

def generate_7d_petrie_rosette():
    """Проекция 2 187 узлов 7D-симплекса на плоскость Петри с 14-кратной симметрией."""
    print("=" * 88)
    print("3. ГЕНЕРАЦИЯ 14-ЛУЧЕВОЙ РОЗЕТКИ ПЕТРИ ('kretov_7d_rosette.png')")
    print("=" * 88)

    dim = 7
    nodes = np.array(list(itertools.product([-1, 0, 1], repeat=dim)))
    charges = np.sum(nodes, axis=1)

    # Ортогональная проекция Петри для 7-мерного симплекса (14-кратная поворотная симметрия)
    angles = np.array([np.pi * k / dim for k in range(dim)])
    proj_x = nodes @ np.cos(angles)
    proj_y = nodes @ np.sin(angles)

    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#0b0f19")
    ax.set_facecolor("#0b0f19")

    # Отрисовка всех 2 187 узлов с цветовой кодировкой по топологическому заряду Q
    scatter = ax.scatter(
        proj_x, proj_y,
        c=charges,
        cmap="coolwarm",
        s=28,
        alpha=0.82,
        edgecolors="none",
        zorder=3
    )

    # Выделение центрального нулевого аттрактора (0,0,0,0,0,0,0)
    ax.scatter((0,), (0,), color="gold", s=220, edgecolors="white", linewidth=1.5, zorder=5,
               label="Центральный узел равновесия (0^7)")

    cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Суммарный топологический заряд Q", color="white", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    ax.set_title("The Kretov Matrix (3⁷ = 2,187 States): 14-Fold Petrie Rosette Projection",
                 color="white", fontsize=13, pad=16)
    ax.axis("off")
    ax.legend(loc="upper right", facecolor="#161b22", edgecolor="gray", labelcolor="white", fontsize=9)

    plt.tight_layout()
    plt.savefig("kretov_7d_rosette.png", dpi=300, facecolor=fig.get_facecolor())
    print("Готово! Изображение сохранено в файл 'kretov_7d_rosette.png'.")
    plt.show()

if __name__ == "__main__":
    run_7d_scaling_audit()
    test_7d_system_stability()
    generate_7d_petrie_rosette() 
