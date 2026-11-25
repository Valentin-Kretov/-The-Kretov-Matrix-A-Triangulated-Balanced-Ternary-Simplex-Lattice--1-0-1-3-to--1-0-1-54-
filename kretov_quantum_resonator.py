import numpy as np


def build_omega3_adjacency():
    r"""
    Построение точной матрицы смежности A (27x27) 54-реберного графа Omega_3 = {-1, 0, +1}^3
    через кронекерово произведение одномерных путей P_3.
    """
    p3 = np.diag([1.0, 1.0], k=1) + np.diag([1.0, 1.0], k=-1)
    eye3 = np.eye(3, dtype=float)

    adj = (
        np.kron(np.kron(p3, eye3), eye3)
        + np.kron(np.kron(eye3, p3), eye3)
        + np.kron(np.kron(eye3, eye3), p3)
    )

    assert adj.shape == (27, 27)
    assert int(round(np.sum(adj))) == 108
    return adj


def simulate_single_cell_breathing():
    r"""
    Эксперимент 1: Унитарная квантовая эволюция одиночного импульса |psi(t)> = exp(-i A t)|psi(0)>,
    запущенного в центральный фокусный узел (0,0,0) (индекс 13).
    - На t = T/8: равномерное распределение по оболочкам (1/8, 3/8, 3/8, 1/8).
    - На t = T/4: 100% энергии фокусируется на 8 полярных вершинах (0, 0, 0, 1).
    - На t = T/2: 100% энергии возвращается в центр (0,0,0) с инверсией фазы (-1).
    - На t = T = pi * sqrt(2): полный спинорный возврат (+1) в (0,0,0).
    """
    adj = build_omega3_adjacency()
    evals, evecs = np.linalg.eigh(adj)

    psi0 = np.zeros(27, dtype=complex)
    psi0.put(13, 1.0 + 0.0j)

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

    # t = T/8: равновесное распределение (1/8, 3/8, 3/8, 1/8)
    _, probs_eighth = evolve(period / 8.0)
    p_center_e = float(np.sum(probs_eighth * (r2_arr == 0)))
    p_faces_e = float(np.sum(probs_eighth * (r2_arr == 1)))
    p_edges_e = float(np.sum(probs_eighth * (r2_arr == 2)))
    p_corners_e = float(np.sum(probs_eighth * (r2_arr == 3)))

    # t = T/4: 100% энергии на 8 полярных вершинах
    _, probs_quarter = evolve(period / 4.0)
    p_corners_quarter = float(np.sum(probs_quarter * (r2_arr == 3)))
    p_center_quarter = float(np.sum(probs_quarter * (r2_arr == 0)))

    # t = T/2: 100% энергии в центре со спинорной инверсией фазы (-1)
    psi_half, probs_half = evolve(period / 2.0)
    p_center_half = float(np.sum(probs_half * (r2_arr == 0)))
    phase_half = float(np.real(psi_half.take(13)))

    # t = T: полный возврат (+1) в (0,0,0)
    psi_full, probs_full = evolve(period)
    p_center_full = float(np.sum(probs_full * (r2_arr == 0)))
    phase_full = float(np.real(psi_full.take(13)))
    norm_full = float(np.sum(probs_full))

    return {
        "period": period,
        "norm_preserved": norm_full,
        "eighth_shells": (p_center_e, p_faces_e, p_edges_e, p_corners_e),
        "quarter_corners_prob": p_corners_quarter,
        "quarter_center_prob": p_center_quarter,
        "half_center_prob": p_center_half,
        "half_phase": phase_half,
        "full_revival_prob": p_center_full,
        "full_phase": phase_full,
    }


def simulate_bipartite_rabi_transfer(coupling_j=None):
    r"""
    Эксперимент 2: Резонансный туннельный перенос кванта энергии между двумя
    связанными 27-узловыми ячейками Omega_3^(A) <-> Omega_3^(B) (54 узла).
    """
    if coupling_j is None:
        coupling_j = float(np.sqrt(2.0) / 20.0)

    adj = build_omega3_adjacency()
    eye2 = np.eye(2, dtype=float)
    sigma_x = np.fliplr(eye2)
    h_54 = np.kron(eye2, adj) + coupling_j * np.kron(sigma_x, np.eye(27, dtype=float))
    assert h_54.shape == (54, 54)

    evals, evecs = np.linalg.eigh(h_54)

    psi0 = np.zeros(54, dtype=complex)
    psi0.put(13, 1.0 + 0.0j)

    t_transfer = float(np.pi / (2.0 * coupling_j))
    phases = np.exp(-1j * evals * t_transfer)
    psi_t = evecs @ (phases * (evecs.T @ psi0))
    probs = np.abs(psi_t) ** 2

    max_center_b = float(probs.take(40))
    max_total_b = float(np.sum(probs.take(np.arange(27, 54))))

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
    br = res.get("breathing")
    rb = res.get("rabi")
    ns = res.get("noise")

    print("=== АУДИТ КВАНТОВОГО РЕЗОНАТОРА МАТРИЦЫ КРЕТОВА (Omega_3) ===\n")
    print(f"Спинорный период де Бройля T = pi * sqrt(2) = {br.get('period'):.6f}")
    print(f"Сохранение полной вероятности (унитарность):    {br.get('norm_preserved'):.8f}")
    c_e, f_e, e_e, v_e = br.get("eighth_shells")
    print(f"Распределение на t = T/8 (центр/грани/ребра/углы): {c_e:.4f} / {f_e:.4f} / {e_e:.4f} / {v_e:.4f}")
    print(f"Фокусировка на 8 углах на t = T/4:               {br.get('quarter_corners_prob')*100:.4f}%")
    print(f"Возврат в центр на t = T/2 (фаза {br.get('half_phase'):+.1f}):         {br.get('half_center_prob')*100:.4f}%")
    print(f"Полный спинорный возврат на t = T (фаза {br.get('full_phase'):+.1f}):   {br.get('full_revival_prob')*100:.4f}%\n")

    print(f"[Двухъячеечный туннельный перенос Omega_3 <-> Omega_3, J = {rb.get('coupling_j'):.5f}]")
    print(f"  Макс. перекачка энергии во вторую ячейку:      {rb.get('max_total_b_prob')*100:.2f}%")
    print(f"  Макс. фокусировка в центре (0,0,0)_B:          {rb.get('max_center_b_prob')*100:.2f}%\n")

    print(f"[Устойчивость кванта к шуму вакуума sigma = {ns.get('noise_sigma')}]")
    print(f"  Средняя точность возврата после цикла T:       {ns.get('mean_revival_fidelity')*100:.2f}%")
