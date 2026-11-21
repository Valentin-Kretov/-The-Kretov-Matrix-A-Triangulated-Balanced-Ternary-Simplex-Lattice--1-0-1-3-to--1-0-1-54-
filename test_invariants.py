import itertools
import numpy as np


def test_lattice_topology_and_spectrum():
    # 1. Generate 27 nodes of {-1, 0, +1}^3
    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    assert len(nodes) == 27

    # 2. Check topological charge Q = x + y + z distribution: {1, 3, 6, 7, 6, 3, 1}
    charges = [sum(node) for node in nodes]
    counts = [charges.count(k) for k in range(-3, 4)]
    assert counts == [1, 3, 6, 7, 6, 3, 1]

    # 3. Verify 54 edges (Manhattan distance == 1) and degree hierarchy (8, 12, 6, 1)
    adj = np.zeros((27, 27), dtype=float)
    for i in range(27):
        for j in range(i + 1, 27):
            dist = sum(abs(nodes[i][d] - nodes[j][d]) for d in range(3))
            if dist == 1:
                adj[i, j] = adj[j, i] = 1.0

    num_edges = int(np.sum(adj) // 2)
    assert num_edges == 54

    degrees = sorted([int(np.sum(adj[i])) for i in range(27)])
    assert degrees.count(3) == 8   # Extremal polar vertices
    assert degrees.count(4) == 12  # Edge midpoints
    assert degrees.count(5) == 6   # Stratum-face centers
    assert degrees.count(6) == 1   # Central focal hub (0,0,0)


def test_fundamental_constants_accuracy():
    # Inverse Fine-Structure Constant (alpha^-1)
    alpha_inv_calc = (4 * np.pi**3 + np.pi**2 + np.pi) - 1.0 / (54.0 * 60.0)
    alpha_inv_pdg = 137.035999
    assert abs(alpha_inv_calc - alpha_inv_pdg) / alpha_inv_pdg < 1e-7

    # Weak Mixing Angle (sin^2 theta_W)
    sin2_tw_calc = 3.0 / 13.0 + 1.0 / (3**7)
    sin2_tw_pdg = 0.231220
    assert abs(sin2_tw_calc - sin2_tw_pdg) / sin2_tw_pdg < 1e-4

    # Strong Coupling Constant (alpha_s)
    alpha_s_calc = (1.0 / (6.0 * np.sqrt(2.0))) * (1.0 + 1.0 / (3**6))
    alpha_s_pdg = 0.118000
    assert abs(alpha_s_calc - alpha_s_pdg) / alpha_s_pdg < 2e-4

    # Quark Cabibbo Angle (theta_12^CKM in degrees)
    cabibbo_rad = np.arcsin(1.0 / np.sqrt(20.0)) + 1.0 / (27.0 * 18.0)
    cabibbo_deg = np.degrees(cabibbo_rad)
    assert abs(cabibbo_deg - 13.0400) < 0.002

    # Solar Neutrino Mixing Angle (theta_12^PMNS in degrees)
    solar_rad = np.arcsin(np.sqrt(1.0 / 3.0 - 1.0 / (18.0 * np.sqrt(3.0))))
    solar_deg = np.degrees(solar_rad)
    assert abs(solar_deg - 33.41) < 0.15


def test_cglmp_bell_bound():
    # Two-qutrit CGLMP maximum quantum violation vs Tsirelson qubit bound
    i3_qutrit = 4.0 / (6.0 * np.sqrt(3.0) - 9.0)
    tsirelson_qubit = 2.0 * np.sqrt(2.0)
    assert i3_qutrit > tsirelson_qubit
    assert abs(i3_qutrit - 2.87293) < 1e-4


if __name__ == "__main__":
    test_lattice_topology_and_spectrum()
    test_fundamental_constants_accuracy()
    test_cglmp_bell_bound()
    print("ALL KRETOV MATRIX INVARIANTS VERIFIED SUCCESSFULLY!")
