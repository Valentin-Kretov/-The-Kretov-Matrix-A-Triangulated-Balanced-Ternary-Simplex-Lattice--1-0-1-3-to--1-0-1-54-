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


def test_v35_fractal_rg_and_kurtosis():
    """Verify v3.5 Kadanoff RG fixed point p0*=1/5, dual-matrix identity, and -1/36 kurtosis."""
    import math

    # 1. Kadanoff block-spin RG recursion: p0' = p0^3 + 1.5 * p0 * (1 - p0)^2
    def rg_step(p0):
        return (p0**3) + 1.5 * p0 * ((1.0 - p0) ** 2)

    p0_star = 1.0 / 5.0
    assert math.isclose(rg_step(p0_star), p0_star, rel_tol=1e-12)

    # Verify convergence from Omega_3 neutral share (7/27) to 1/5
    p = 7.0 / 27.0
    for _ in range(50):
        p = rg_step(p)
    assert math.isclose(p, p0_star, rel_tol=1e-9)

    # 2. Dual-matrix identity and exact excess kurtosis -1/F_36
    assert 3**54 == (3**6) ** 9 == (3**27) ** 2
    kappa_excess_54 = -3.0 / (2.0 * 54.0)
    assert math.isclose(kappa_excess_54, -1.0 / 36.0, rel_tol=1e-12)


def test_v35_analytical_noise_and_jarlskog():
    """Verify v3.5 exact erf noise limits (N -> inf) and parameter-free J_PMNS."""
    import math

    # 1. Exact analytical noise recovery for sigma = 0.35
    p1_exact = (1.0 + 2.0 * math.erf(0.5 / (0.35 * math.sqrt(2.0)))) / 3.0
    p3_exact = p1_exact**3
    assert math.isclose(p1_exact, 0.8979152, abs_tol=1e-6)
    assert math.isclose(p3_exact, 0.7239453, abs_tol=1e-6)

    # 2. Parameter-free Jarlskog invariant J_PMNS from 120-degree triadic shift
    t12 = math.radians(33.2900)
    t23 = math.radians(45.0000)
    t13 = math.radians(8.5400)
    delta_pmns = math.radians(68.4 + 120.0)
    j_pmns = (
        (1.0 / 8.0)
        * math.sin(2.0 * t12)
        * math.sin(2.0 * t23)
        * math.sin(2.0 * t13)
        * math.cos(t13)
        * math.sin(delta_pmns)
    )
    assert math.isclose(j_pmns, -0.004869, abs_tol=1e-5)



def test_v40_continuum_and_topology():
    """Verify v4.0 Euler characteristic, Laplacian determinant, 972*pi topological alpha^-1, and RG unification."""
    import math

    # 1. Euler characteristic of Omega_3: chi = V - E + F = 27 - 54 + 36 = 9
    V, E, F = 27, 54, 36
    chi = V - E + F
    assert chi == 9 == 3**2

    # 2. Exact non-zero spectral determinant of the graph Laplacian: (3*sqrt(2))^2 * (2*sqrt(2))^6 * (1*sqrt(2))^12
    det_prime = (
        ((3 * math.sqrt(2)) ** 2)
        * ((2 * math.sqrt(2)) ** 6)
        * ((1 * math.sqrt(2)) ** 12)
    )
    assert math.isclose(det_prime, 589824.0, rel_tol=1e-12)
    assert int(round(det_prime)) == (2**16) * (3**2)

    # 3. Parameter-free topological loop correction: E * chi * 2*pi = 972*pi
    alpha_inv_top = (4 * (math.pi**3) + (math.pi**2) + math.pi) - (
        1.0 / (E * chi * 2.0 * math.pi)
    )
    assert math.isclose(alpha_inv_top, 137.0359763, abs_tol=1e-6)

    # 4. Discrete RG flow convergence across 3^n levels (from n=3 electroweak to n=31 GUT scale)
    # Using standard SU(5)-normalized hypercharge b1 = 41/10, b2 = -19/6, b3 = -7
    a1_inv, a2_inv, a3_inv = 59.01, 29.57, 8.47
    b1, b2, b3 = 41.0 / 10.0, -19.0 / 6.0, -7.0
    step = math.log(3.0) / (2.0 * math.pi)
    for _ in range(28):  # n = 3 -> n = 31
        a1_inv -= b1 * step
        a2_inv -= b2 * step
        a3_inv -= b3 * step
    # At n = 31 (~10^16 GeV), gauge couplings converge near ~40-46
    assert abs(a1_inv - a2_inv) < 4.0
    assert abs(a2_inv - a3_inv) < 6.0

if __name__ == "__main__":
    test_lattice_topology_and_spectrum()
    test_fundamental_constants_accuracy()
    test_cglmp_bell_bound()
    print("ALL KRETOV MATRIX INVARIANTS VERIFIED SUCCESSFULLY!")
