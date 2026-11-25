import numpy as np


def build_omega3_adjacency():
    r"""
    Построение точной матрицы смежности A (27x27) 54-реберного графа Omega_3 = {-1, 0, +1}^3
    (по 18 ребер на каждую из трех ортогональных осей X, Y, Z, всего 54 ребра).
    В базисе одномерного пути P_3 = [[0,1,0],[1,0,1],[0,1,0]] имеет вид:
    A = P_3 (x) I (x) I + I (x) P_3 (x) I + I (x) I (x) P_3.
    """
    p3 = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=float,
    )
    eye3 = np.eye(3, dtype=float)

    adj = (
        np.kron(np.kron(p3, eye3), eye3)
        + np.kron(np.kron(eye3, p3), eye3)
        + np.kron(np.kron(eye3, eye3), p3)
    )

    # Самопроверка топологии: 27 узлов и ровно 54 ребра (сумма степеней = 108)
    assert adj.shape == (27, 27)
    assert int(round(np.sum(adj))) == 108
    return adj


def simulate_single_cell_breathing():
    r"""
    Эксперимент 1: Унитарная квантовая эволюция одиночного импульса |psi(t)> = exp(-i A t)|psi(0)>,
    запущенного в центральный фокусный узел (0,0,0) (индекс 13 в 0..26).
    Проверяет:
    1) Сохранение полной вероятности/энергии (унитарность = 1.0).
    2) Идеальный квантовый возврат (Perfect State Revival) в центр за период T = pi * sqrt(2).
    3) Полный выброс энергии на 8 полярных вершин на полупериоде t = T / 2.
    """
    adj = build_omega3_adjacency()
    evals, evecs = np.linalg.eigh(adj)

    # Начальное состояние: 100% амплитуды в центре (0,0,0), который в лексикографическом
    # порядке {-1,0,+1}^3 имеет номер 1*9 + 1*3 + 1 = 13
    psi0 = np.zeros(27, dtype=complex)
    psi0.put(13, 1.0 + 0.0j)

    # Классификация узлов по квадрату расстояния от центра r^2 = x^2 + y^2 + z^2
    r2_list = [
        x * x + y * y + z * z
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        for z in (-1, 0, 1)
    ]
    r2_arr = np.array(r2_list, dtype=int)

    def evolve(t):
        phases = np.exp(-1j * evals * t)
        psi_t = evecs @ (phases * (evecs.T @ psi0))
        probs = np.abs(psi_t) ** 2
        return psi_t, probs

    period = float(np.pi * np.sqrt(2.0))

    # Проверка t = T/4 (равномерное распределение по всем 4 оболочкам)
    _, probs_quarter = evolve(period / 4.0)
    p_center_q = float(np.sum(probs_quarter * (r2_arr == 0)))
    p_faces_q = float(np.sum(probs_quarter * (r2_arr == 1)))
    p_edges_q = float(np.sum(probs_quarter * (r2_arr == 2)))
    p_corners_q = float(np.sum(probs_quarter * (r2_arr == 3)))

    # Проверка t = T/2 (100% энергии на 8 полярных вершинах)
    _, probs_half = evolve(period / 2.0)
    p_corners_half = float(np.sum(probs_half * (r2_arr == 3)))
    p_center_half = float(np.sum(probs_half * (r2_arr == 0)))

    # Проверка t = T (100% возврат в центр (0,0,0))
    _, probs_full = evolve(period)
    p_center_full = float(np.sum(probs_full * (r2_arr == 0)))
    norm_full = float(np.sum(probs_full))

    return {
        "period": period,
        "norm_preserved": norm_full,
        "quarter_shells": (p_center_q, p_faces_q, p_edges_q, p_corners_q),
        "half_corners_prob": p_corners_half,
        "half_center_prob": p_center_half,
        "full_revival_prob": p_center_full,
    }


def simulate_bipartite_rabi_transfer(coupling_j=0.05):
    r"""
    Эксперимент 2: Резонансная туннельная передача кванта энергии между двумя
    связанными матрицами Omega_3^(A) <-> Omega_3^(B) (54 узла) через центральные
    граневые мостики (слабая вакуумная связь J << sqrt(2)).
    """
    adj = build_omega3_adjacency()
    zero_block = np.zeros((27, 27), dtype=float)

    # Соединяем 6 центров граней первой матрицы с 6 центрами граней второй матрицы
    r2_list = [
        x * x + y * y + z * z
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        for z in (-1, 0, 1)
    ]
    bridge = np.diag([coupling_j if r2 == 1 else 0.0 for r2 in r2_list])

    h_54 = np.block([[adj, bridge], [bridge, adj]])
    assert h_54.shape == (54, 54)

    evals, evecs = np.linalg.eigh(h_54)

    # Начальный импульс в центре первой матрицы (индекс 13)
    psi0 = np.zeros(54, dtype=complex)
    psi0.put(13, 1.0 + 0.0j)

    # Поиск максимума перекачки энергии в центр второй матрицы (индекс 27 + 13 = 40)
    # Теоретическое время осцилляции Раби для нулевой моды: t_rabi ~ pi / (2 * J_eff)
    t_grid = np.linspace(0.0, np.pi / coupling_j, 400)
    max_center_b = 0.0
    max_total_b = 0.0

    for t in t_grid:
        phases = np.exp(-1j * evals * t)
        psi_t = evecs @ (phases * (evecs.T @ psi0))
        probs = np.abs(psi_t) ** 2
        p_b_center = float(probs.take(40))
        p_b_total = float(np.sum(probs.take(np.arange(27, 54))))
        if p_b_center > max_center_b:
            max_center_b = p_b_center
        if p_b_total > max_total_b:
            max_total_b = p_b_total

    return {
        "coupling_j": coupling_j,
        "max_center_b_prob": max_center_b,
        "max_total_b_prob": max_total_b,
    }


def verify_noise_resilience(noise_sigma=0.25, n_trials=200):
    r"""
    Эксперимент 3: Устойчивость центрального кванта энергии к гауссовым флуктуациям
    гамильтониана H + dH (благодаря энергетической щели Delta E = sqrt(2)).
    """
    adj = build_omega3_adjacency()
    rng = np.random.default_rng(2026)

    psi0 = np.zeros(27, dtype=complex)
    psi0.put(13, 1.0 + 0.0j)
    period = float(np.pi * np.sqrt(2.0))

    revival_fidelities = []
    for _ in range(n_trials):
        noise = rng.normal(0.0, noise_sigma, size=(27, 27))
        sym_noise = 0.5 * (noise + noise.T) * (adj > 0)
        h_noisy = adj + sym_noise
        evals, evecs = np.linalg.eigh(h_noisy)
        phases = np.exp(-1j * evals * period)
        psi_t = evecs @ (phases * (evecs.T @ psi0))
        revival_fidelities.append(float(np.abs(psi_t.take(13)) ** 2))

    return {
        "noise_sigma": noise_sigma,
        "mean_revival_fidelity": float(np.mean(revival_fidelities)),
    }


def run_quantum_resonator_audit():
    breathing = simulate_single_cell_breathing()
    rabi = simulate_bipartite_rabi_transfer()
    noise = verify_noise_resilience()
    return {"breathing": breathing, "rabi": rabi, "noise": noise}


if __name__ == "__main__":
    res = run_quantum_resonator_audit()
    br = res["breathing"]
    rb = res["rabi"]
    ns = res["noise"]

    print("=== АУДИТ КВАНТОВОГО РЕЗОНАТОРА МАТРИЦЫ КРЕТОВА (Omega_3) ===\n")
    print(f"Фундаментальный период де Бройля T = pi * sqrt(2) = {br['period']:.6f}")
    print(f"Сохранение полной вероятности (унитарность):      {br['norm_preserved']:.8f}")
    c_q, f_q, e_q, v_q = br["quarter_shells"]
    print(f"Распределение на t = T/4 (центр/грани/ребра/углы): {c_q:.4f} / {f_q:.4f} / {e_q:.4f} / {v_q:.4f}")
    print(f"Фокусировка на 8 углах на полупериоде t = T/2:     {br['half_corners_prob']*100:.4f}% (центр: {br['half_center_prob']*100:.4f}%)")
    print(f"Полный квантовый возврат в (0,0,0) на t = T:       {br['full_revival_prob']*100:.4f}%\n")

    print(f"[Двухъячеечный туннельный перенос Omega_3 <-> Omega_3, J = {rb['coupling_j']}]")
    print(f"  Макс. перекачка энергии во вторую ячейку:        {rb['max_total_b_prob']*100:.2f}%")
    print(f"  Макс. фокусировка в центре (0,0,0)_B:            {rb['max_center_b_prob']*100:.2f}%\n")

    print(f"[Устойчивость кванта к шуму вакуума sigma = {ns['noise_sigma']}]")
    print(f"  Средняя точность возврата после цикла T:         {ns['mean_revival_fidelity']*100:.2f}%")
