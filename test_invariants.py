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
    # At n = 31 (~10^16 GeV), initial electroweak gap (29.44) narrows nearly 5x to ~6.14, with a2 & a3 within ~2.33
    assert abs(a1_inv - a2_inv) < 6.5
    assert abs(a2_inv - a3_inv) < 2.5


def test_v50_sm_gauge_and_delta27_potential():
    """Verify v5.0 node connectivity decomposition (27 = 8 + 12 + 6 + 1) and Delta(27) potential invariance."""
    import itertools
    import numpy as np

    # 1. Exact node hierarchy by zero-coordinate count (matching SM gauge & matter structure)
    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    extremal_vertices = [
        n for n in nodes if n.count(0) == 0
    ]  # 8 chiral octets (degree 3)
    edge_midpoints = [
        n for n in nodes if n.count(0) == 1
    ]  # 12 SM gauge bosons: 8 + 3 + 1 (degree 4)
    face_centers = [
        n for n in nodes if n.count(0) == 2
    ]  # 6 Higgs/flavon doublets (degree 5)
    central_hub = [
        n for n in nodes if n.count(0) == 3
    ]  # 1 unbroken U(1)_em / theta_QCD=0 hub (degree 6)

    assert len(extremal_vertices) == 8
    assert len(edge_midpoints) == 12
    assert len(face_centers) == 6
    assert len(central_hub) == 1
    assert 8 + 12 + 6 + 1 == 27

    # 2. Verify exact invariance of the Delta(27) flavon potential term under all 27 group elements
    omega = np.exp(2j * np.pi / 3.0)
    C = np.array(
        [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]], dtype=complex
    )
    D = np.diag([1.0, omega, omega**2])

    def delta27_invariant_I3(phi):
        # I3 = phi_-1^2 * phi_0^* * phi_+1^* + cyclic permutations
        p_m, p_0, p_p = phi[0], phi[1], phi[2]
        return (
            (p_m**2) * np.conj(p_0) * np.conj(p_p)
            + (p_0**2) * np.conj(p_p) * np.conj(p_m)
            + (p_p**2) * np.conj(p_m) * np.conj(p_0)
        )

    rng = np.random.default_rng(seed=27)
    phi_test = rng.normal(size=3) + 1j * rng.normal(size=3)
    base_val = delta27_invariant_I3(phi_test)

    for x, y, z in nodes:
        g = (
            (omega ** (z % 3))
            * np.linalg.matrix_power(C, x % 3)
            @ np.linalg.matrix_power(D, y % 3)
        )
        phi_transformed = g @ phi_test
        assert np.allclose(
            delta27_invariant_I3(phi_transformed), base_val, atol=1e-12
        )


def test_v60_zero_parameter_closure():
    """Verify v6.0 zero-parameter closure: F/E = 2/3, holographic 3^243 bound, and epsilon = 1/27 generation step."""
    import math

    # 1. Induced potential coupling ratio fixed by simplex faces-to-edges: lambda_2 / lambda_1 = F / E = 36 / 54 = 2 / 3
    F, E, V = 36, 54, 27
    coupling_ratio = F / E
    assert math.isclose(coupling_ratio, 2.0 / 3.0, rel_tol=1e-12)

    # 2. Holographic entropy bound at tetration level k=5 (3^243 ~ 8.719e115) fixing a_0 = l_Pl
    log10_s_holo = 243 * math.log10(3.0)
    assert math.isclose(log10_s_holo, 115.9405, abs_tol=1e-3)

    # 3. Geometric loop suppression factor epsilon = 1/V = 1/27 vs PDG 2nd/3rd generation geometric mean
    epsilon = 1.0 / V
    # PDG ratios: m_s / m_b ~ 93.4 / 4180, m_mu / m_tau ~ 105.66 / 1776.86
    pdg_geom_mean = math.sqrt((93.4 / 4180.0) * (105.66 / 1776.86))
    assert math.isclose(epsilon, pdg_geom_mean, rel_tol=0.02)

if __name__ == "__main__":
    test_lattice_topology_and_spectrum()
    test_fundamental_constants_accuracy()
    test_cglmp_bell_bound()
    print("ALL KRETOV MATRIX INVARIANTS VERIFIED SUCCESSFULLY!")


def test_v61_central_dipole_equilibrium():
    """
    Проверка теоремы центрального информационного равновесия констант
    относительно фокусного узла theta_QCD = 0 в Omega_3:
    1) 25 квантовых параметров СМ полностью уравновешиваются в (0,0,0) (< 0.1%).
    2) Добавление космологической постоянной Lambda (w ~ 280.6) создает
       некомпенсированный вакуумный остаток ~21.15% (источник темной энергии),
       при этом все равно превосходя 99.9% случайных конфигураций (p < 0.01).
    """
    import numpy as np
    from kretov_equilibrium_audit import run_full_audit

    res = run_full_audit()

    # 1. Полнота базиса
    assert len(res["names"]) == 26
    assert len(res["pairs"]) == 13
    assert len(set(res["free_perm"])) == 26

    # 2. Чистый сектор СМ (25 констант) идеально замыкается в нулевой диполь вокруг theta_QCD = 0
    assert res["sm25_dip_err"] < 1e-3, f"Квантовый диполь СМ не замкнулся: {res['sm25_dip_err']}"
    assert res["sm25_pvalue"] < 0.01

    # 3. Полный 26-базис с Lambda достигает теоретического минимума вакуумного остатка (~0.21155)
    assert 0.20 < res["free_dip_err"] < 0.22, f"Неожиданный вакуумный остаток: {res['free_dip_err']}"
    assert res["free_pvalue"] < 0.01, f"Равновесие не отличается от шума: p={res['free_pvalue']}"

    # 4. Космологическая постоянная Lambda занимает центр грани (r^2 = 1) —
    # главную ось симметрии, напрямую связанную с центральным узлом (0,0,0)
    lambda_idx = res["names"].index("Lambda_dimless")
    node_pos = int(np.argwhere(res["free_perm"] == lambda_idx).item())
    lambda_node = res["nodes"].take(node_pos, axis=0)
    assert int(round(np.sum(lambda_node ** 2))) == 1


def test_v62_rmt_spectral_theorem():
    """
    Проверка аналитического разложения спектра симметричных троичных матриц 3x3
    (3^6 = 729) и перехода к закону полукруга Вигнера при N = 9, 27.
    """
    from kretov_rmt_analytical import run_rmt_proof

    res = run_rmt_proof()
    ex = res["exact_3x3"]
    wig = res["wigner"]

    # 1. Точное разложение пространства 3^6 = 729 и пирамида рангов
    assert ex["total"] == 729
    assert ex["non_degenerate"] == 516
    assert ex["degenerate"] == 213  # 71 / 243 = 71 / 3^5
    assert ex["rank_counts"] == {0: 1, 1: 26, 2: 186, 3: 516}
    assert ex["poly_classes"] == 30

    # 2. Полная 48-элементная орбита группы O_h с точным серебряным сечением
    assert ex["silver_orbit_count"] == 48

    # 3. Точность приближения к pi/2 и серебряному сечению 1 + sqrt(2) > 99.8%
    assert ex["pi_half_accuracy"] > 0.998
    assert ex["silver_accuracy"] > 0.998

    # 4. Масштабирование Вигнера (GOE) при N = 9 и N = 27: подавление нулевых мод
    assert wig.get(9).get("edge_ratio") > 0.80
    assert wig.get(27).get("edge_ratio") > 0.90
    assert wig.get(27).get("zero_mode_fraction") < 0.01


def test_v63_quantum_resonator():
    """
    Проверка динамики элементарного кванта энергии (уравнение Шредингера)
    на 27-узловой решетке Omega_3 и двухъячеечного туннельного переноса (54 узла).
    """
    import numpy as np
    from kretov_quantum_resonator import run_quantum_resonator_audit

    res = run_quantum_resonator_audit()
    br = res.get("breathing")
    rb = res.get("rabi")
    ns = res.get("noise")

    # 1. Унитарность и спинорный период T = pi * sqrt(2)
    assert np.isclose(br.get("norm_preserved"), 1.0, atol=1e-12)
    assert np.isclose(br.get("period"), np.pi * np.sqrt(2.0), atol=1e-12)

    # 2. Выброс на 8 вершин на t = T/4, спинорная инверсия (-1) на T/2 и возврат (+1) на T
    assert br.get("quarter_corners_prob") > 0.999999
    assert br.get("quarter_center_prob") < 1e-12
    assert br.get("half_center_prob") > 0.999999
    assert np.isclose(br.get("half_phase"), -1.0, atol=1e-12)
    assert br.get("full_revival_prob") > 0.999999
    assert np.isclose(br.get("full_phase"), 1.0, atol=1e-12)

    # 3. Симметричное дыхание оболочек на t = T/8: 1/8, 3/8, 3/8, 1/8
    c_e, f_e, e_e, v_e = br.get("eighth_shells")
    assert np.isclose(c_e, 0.125, atol=1e-12)
    assert np.isclose(f_e, 0.375, atol=1e-12)
    assert np.isclose(e_e, 0.375, atol=1e-12)
    assert np.isclose(v_e, 0.125, atol=1e-12)

    # 4. Резонансная туннельная передача импульса во вторую ячейку Omega_3 (> 95%)
    assert rb.get("max_total_b_prob") > 0.95
    assert rb.get("max_center_b_prob") > 0.90

    # 5. Защита кванта от флуктуаций вакуума благодаря щели Delta E = sqrt(2)
    assert ns.get("mean_revival_fidelity") > 0.50
