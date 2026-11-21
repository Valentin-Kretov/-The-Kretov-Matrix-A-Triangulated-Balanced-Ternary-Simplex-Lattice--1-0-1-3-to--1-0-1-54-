import itertools
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

def analyze_graph_topology_and_spectrum():
    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    n_nodes = len(nodes)
    adj_matrix = np.zeros((n_nodes, n_nodes), dtype=int)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if sum(abs(a - b) for a, b in zip(nodes[i], nodes[j])) == 1:
                adj_matrix[i, j] = adj_matrix[j, i] = 1
    eigenvalues = np.linalg.eigvalsh(adj_matrix)
    print("Graph spectrum computed:", len(eigenvalues), "levels.")

def test_qutrit_nonlocality():
    print("CGLMP I_3:", 4.0 / (6.0 * np.sqrt(3) - 9.0))

def test_arrow_of_time(n_walkers=100_000, steps=100, seed=42):
    rng = np.random.default_rng(seed)
    moves = rng.choice([-1, 0, 1], size=(n_walkers, steps, 3))
    positions = np.cumsum(moves, axis=1)
    returned = np.any(np.all(positions == 0, axis=2), axis=1)
    print(f"3D non-return prob: {100.0 - np.mean(returned)*100:.2f}%")

def analyze_fractal_ladder():
    kernel = np.ones(3, dtype=int)
    for n in range(7):
        if n == 0:
            z = 1
        else:
            poly = np.ones(1, dtype=int)
            for _ in range(n):
                poly = np.convolve(poly, kernel)
            z = poly[n]
        print(f"3^{n} = {3**n} | Q=0: {z}")

def run_stress_tests(seed=42):
    rng = np.random.default_rng(seed)
    clean = rng.choice([-1, 0, 1], size=(1_000_000, 3))
    noisy = clean + rng.normal(0, 0.35, size=(1_000_000, 3))
    recovered = np.clip(np.round(noisy), -1, 1).astype(int)
    print(f"Noise recovery: {np.mean(np.all(clean == recovered, axis=1))*100:.2f}%")

def predict_neutrino_masses():
    dm2_21, dm2_31 = 7.42e-5, 2.515e-3
    def koide_nu(m1):
        m2, m3 = np.sqrt(m1**2 + dm2_21), np.sqrt(m1**2 + dm2_31)
        return ((m1 + m2 + m3) / (-np.sqrt(m1) + np.sqrt(m2) + np.sqrt(m3)) ** 2) - (2.0 / 3.0)
    sol = root_scalar(koide_nu, bracket=[1e-6, 0.1], method="brentq")
    m1 = sol.root
    m2, m3 = np.sqrt(m1**2 + dm2_21), np.sqrt(m1**2 + dm2_31)
    print(f"Neutrino sum: {(m1+m2+m3)*1000:.2f} meV")

def visualize_3d_lattice():
    coords = list(itertools.product([-1, 0, 1], repeat=3))
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    for x, y, z in coords:
        if (x, y, z) != (0, 0, 0):
            ax.plot([0, x], [0, y], [0, z], color="gray", alpha=0.2, linewidth=0.8)
    for x, y, z in coords:
        q = x + y + z
        if (x, y, z) == (0, 0, 0):
            ax.scatter(x, y, z, color="gold", s=380, edgecolors="black", linewidth=2, zorder=10,
                       label="27th Constant (0,0,0): theta_QCD = 0")
        elif q == 0:
            ax.scatter(x, y, z, color="limegreen", s=140, edgecolors="black", alpha=0.9,
                       label="Dynamic Zero (Q = 0)" if (x, y, z) == (-1, 0, 1) else "")
        elif q > 0:
            ax.scatter(x, y, z, color="crimson", s=100 + q * 30, alpha=0.75,
                       label="Positive Pole (Q > 0)" if (x, y, z) == (1, 1, 1) else "")
        else:
            ax.scatter(x, y, z, color="royalblue", s=100 + abs(q) * 30, alpha=0.75,
                       label="Negative Pole (Q < 0)" if (x, y, z) == (-1, -1, -1) else "")
    ax.set_title("The Kretov Matrix: Balanced Ternary State Space {-1, 0, +1}^3 (27 Nodes)", fontsize=12, pad=15)
    ax.set_xlabel("Axis X: Dynamics & Forces")
    ax.set_ylabel("Axis Y: Substance & Masses")
    ax.set_zlabel("Axis Z: Geometry & Hidden Sector")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])
    ax.legend(loc="upper left", fontsize=8.5)
    plt.tight_layout()
    plt.savefig("kretov_matrix_3d.png", dpi=300)
    print("Saved kretov_matrix_3d.png")

if __name__ == "__main__":
    analyze_graph_topology_and_spectrum()
    test_qutrit_nonlocality()
    test_arrow_of_time()
    analyze_fractal_ladder()
    run_stress_tests()
    predict_neutrino_masses()
    visualize_3d_lattice()
