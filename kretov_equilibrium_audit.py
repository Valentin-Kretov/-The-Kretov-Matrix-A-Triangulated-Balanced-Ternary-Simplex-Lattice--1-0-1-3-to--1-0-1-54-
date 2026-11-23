import numpy as np


def get_26_dimensionless_constants():
    """
    Формирование строго безразмерного базиса из 26 фундаментальных констант
    Стандартной модели + LambdaCDM (M_Pl = 1.22089e19 ГэВ, v = 246.22 ГэВ).
    """
    M_Pl = 1.22089e19  # ГэВ
    v = 246.22         # ГэВ
    m_H = 125.10       # ГэВ

    def yukawa(m_gev):
        return np.sqrt(2.0) * m_gev / v

    constants = {
        # Слой I: Взаимодействия, вакуум и CP-фазы (9)
        "alpha_em": 1.0 / 137.035999,
        "sin2_thetaW": 0.23122,
        "alpha_s": 0.11800,
        "v_over_MPl": v / M_Pl,
        "lambda_H": (m_H ** 2) / (2.0 * v ** 2),
        "Lambda_dimless": 2.88e-122,
        "delta_CKM": np.deg2rad(68.4),
        "eta_B": 6.14e-10,
        "delta_PMNS": np.deg2rad(188.4),

        # Слой II: Массы заряженных фермионов — юкавские константы (9)
        "y_u": yukawa(2.16e-3),
        "y_c": yukawa(1.27),
        "y_t": yukawa(172.7),
        "y_d": yukawa(4.67e-3),
        "y_s": yukawa(93.4e-3),
        "y_b": yukawa(4.18),
        "y_e": yukawa(0.51099895e-3),
        "y_mu": yukawa(105.6583755e-3),
        "y_tau": yukawa(1.77686),

        # Слой III: Нейтрино и углы смешивания CKM/PMNS (8)
        "y_nu1": yukawa(0.36e-12),
        "y_nu2": yukawa(8.62e-12),
        "y_nu3": yukawa(50.15e-12),
        "theta12_CKM": np.deg2rad(13.04),
        "theta23_CKM": np.deg2rad(2.38),
        "theta13_CKM": np.deg2rad(0.201),
        "theta12_PMNS": np.deg2rad(33.41),
        "theta13_PMNS": np.deg2rad(8.54),
    }
    # Примечание: theta23_PMNS = 45 deg = pi/4 (0.785398 рад) замещает eta_B в 26-параметрическом
    # базисе СМ+LambdaCDM. Для полного соответствия 26 параметрам СМ + Lambda используем точный список:
    constants.pop("eta_B")
    constants["theta23_PMNS"] = np.deg2rad(45.00)

    assert len(constants) == 26, f"Ожидалось 26 констант, получено {len(constants)}"
    assert all(val > 0 for val in constants.values()), "Все константы должны быть строго > 0"
    return constants


def generate_lattice_nodes():
    """
    Генерация 26 внешних узлов {-1, 0, +1}^3 \ {(0,0,0)}
    и проверка наличия 13 точных антиподальных пар.
    """
    nodes = [
        (x, y, z)
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        for z in (-1, 0, 1)
        if (x, y, z) != (0, 0, 0)
    ]
    assert len(nodes) == 26

    node_set = set(nodes)
    pairs = []
    visited = set()
    for v in nodes:
        anti_v = (-v, -v, -v)
        assert anti_v in node_set, f"Отсутствует антипод для узла {v}"
        if v not in visited:
            pairs.append((v, anti_v))
            visited.add(v)
            visited.add(anti_v)

    assert len(pairs) == 13
    return np.array(nodes, dtype=float), pairs


def compute_pairwise_compensation(constants):
    """
    Вариант 1: Аналитический поиск глобального минимума попарной компенсации
    w_a + w_b -> const, где w_i = |ln(X_i)|.
    """
    items = sorted([(k, abs(np.log(v))) for k, v in constants.items()], key=lambda x: x)
    weights = np.array([x for x in items])
    target = 2.0 * np.mean(weights)

    pairs_out = []
    sums = []
    for k in range(13):
        na, wa = items[k]
        nb, wb = items[25 - k]
        s = wa + wb
        sums.append(s)
        pairs_out.append((na, nb, wa, wb, s))

    sums = np.array(sums)
    cv = float(np.std(sums) / np.mean(sums))
    return pairs_out, float(target), cv


def search_3d_equilibrium(constants, nodes, layered_constraint=False, n_restarts=8, steps=60_000):
    """
    Вариант 2: Поиск глобального 3D-равновесия (нулевой дипольный момент в (0,0,0)
    и изотропный тензор инерции).
    Если layered_constraint=True, сохраняется группировка по 3 слоям (X, Y, Z).
    """
    names = list(constants.keys())
    weights = np.array([abs(np.log(constants[k])) for k in names])
    total_w = float(np.sum(weights))

    # Разбиение индексов узлов по слоям X = -1, 0, +1 (9 + 8 + 9 = 26 узлов)
    layer_node_groups = [
        np.where(nodes[:, 0] == -1)[0],
        np.where(nodes[:, 0] == 0)[0],
        np.where(nodes[:, 0] == 1)[0],
    ]
    # Разбиение констант на 3 группы (9 Взаимодействия/CP, 8 Углы/Нейтрино, 9 Фермионы)
    layer_const_groups = [
        np.arange(0, 9),
        np.arange(18, 26),
        np.arange(9, 18),
    ]

    def evaluate(perm):
        w = weights[perm]
        dipole = np.sum(w[:, None] * nodes, axis=0)
        dip_err = float(np.linalg.norm(dipole) / total_w)

        I_xx = np.sum(w * (nodes[:, 1] ** 2 + nodes[:, 2] ** 2))
        I_yy = np.sum(w * (nodes[:, 0] ** 2 + nodes[:, 2] ** 2))
        I_zz = np.sum(w * (nodes[:, 0] ** 2 + nodes[:, 1] ** 2))
        I_xy = -np.sum(w * nodes[:, 0] * nodes[:, 1])
        I_xz = -np.sum(w * nodes[:, 0] * nodes[:, 2])
        I_yz = -np.sum(w * nodes[:, 1] * nodes[:, 2])

        diag_mean = (I_xx + I_yy + I_zz) / 3.0
        aniso = float((np.std([I_xx, I_yy, I_zz]) + abs(I_xy) + abs(I_xz) + abs(I_yz)) / diag_mean)
        return dip_err + 0.1 * aniso, dip_err, aniso, dipole

    best_loss = float("inf")
    best_state = None

    for run in range(n_restarts):
        rng = np.random.default_rng(2026 + run)
        perm = np.zeros(26, dtype=int)

        if layered_constraint:
            for n_grp, c_grp in zip(layer_node_groups, layer_const_groups):
                perm[n_grp] = rng.permutation(c_grp)
        else:
            perm = rng.permutation(26)

        curr_loss, curr_dip, curr_aniso, curr_vec = evaluate(perm)

        for step in range(steps):
            T = 0.02 * ((1e-6 / 0.02) ** (step / steps))
            if layered_constraint:
                g_idx = int(rng.integers(0, 3))
                grp = layer_node_groups[g_idx]
                i, j = rng.choice(grp, size=2, replace=False)
            else:
                i, j = rng.choice(26, size=2, replace=False)

            perm[i], perm[j] = perm[j], perm[i]
            new_loss, new_dip, new_aniso, new_vec = evaluate(perm)

            if new_loss < curr_loss or rng.random() < np.exp((curr_loss - new_loss) / T):
                curr_loss, curr_dip, curr_aniso, curr_vec = new_loss, new_dip, new_aniso, new_vec
                if new_loss < best_loss:
                    best_loss = new_loss
                    best_state = (perm.copy(), new_dip, new_aniso, new_vec.copy())
            else:
                perm[i], perm[j] = perm[j], perm[i]

    best_perm, best_dip, best_aniso, best_vec = best_state
    assert len(set(best_perm)) == 26
    return names, weights, best_perm, best_dip, best_aniso, best_vec


def compute_pvalue(weights, nodes, target_dip_err, n_samples=3000):
    """
    Оценка статистической значимости равновесия против случайных перестановок.
    """
    rng = np.random.default_rng(777)
    total_w = float(np.sum(weights))
    hits = 0
    for _ in range(n_samples):
        p = rng.permutation(weights)
        d = np.linalg.norm(np.sum(p[:, None] * nodes, axis=0)) / total_w
        if d <= target_dip_err:
            hits += 1
    return hits / n_samples


def run_full_audit():
    constants = get_26_dimensionless_constants()
    nodes, _ = generate_lattice_nodes()

    pairs_out, target_s, cv_1 = compute_pairwise_compensation(constants)
    names, weights, perm_free, dip_free, aniso_free, vec_free = search_3d_equilibrium(
        constants, nodes, layered_constraint=False
    )
    _, _, perm_layer, dip_layer, aniso_layer, vec_layer = search_3d_equilibrium(
        constants, nodes, layered_constraint=True
    )
    p_free = compute_pvalue(weights, nodes, dip_free)

    return {
        "pairwise_cv": cv_1,
        "pairwise_target": target_s,
        "pairs": pairs_out,
        "free_dip_err": dip_free,
        "free_aniso": aniso_free,
        "free_vec": vec_free,
        "free_perm": perm_free,
        "free_pvalue": p_free,
        "layered_dip_err": dip_layer,
        "layered_aniso": aniso_layer,
        "layered_vec": vec_layer,
        "layered_perm": perm_layer,
        "names": names,
        "weights": weights,
        "nodes": nodes,
    }


if __name__ == "__main__":
    res = run_full_audit()
    print("=== АУДИТ ЦЕНТРАЛЬНОГО РАВНОВЕСИЯ МАТРИЦЫ КРЕТОВА ===\n")
    print(f"[Вариант 1] Попарная компенсация |ln(X_a)| + |ln(X_b)|:")
    print(f"  Средняя сумма = {res['pairwise_target']:.3f}, отн. разброс = {res['pairwise_cv']*100:.2f}%\n")

    print(f"[Вариант 2A] Свободное 3D-равновесие (без привязки к слоям):")
    print(f"  Остаточный диполь = {res['free_dip_err']:.6e} ({res['free_dip_err']*100:.5f}%)")
    print(f"  Анизотропия инерции = {res['free_aniso']:.6e}")
    print(f"  p-value против шума = {res['free_pvalue']:.5f}\n")

    print(f"[Вариант 2B] Слоистое 3D-равновесие (сохранение слоев X, Y, Z):")
    print(f"  Остаточный диполь = {res['layered_dip_err']:.6e} ({res['layered_dip_err']*100:.5f}%)")
    print(f"  Анизотропия инерции = {res['layered_aniso']:.6e}\n")

    print("Карта узлов (Свободное 3D-равновесие):")
    for node, idx in zip(res["nodes"], res["free_perm"]):
        c = f"({int(node):+d},{int(node):+d},{int(node):+d})"
        print(f"  {c} -> {res['names'][idx]:<15} | |ln(X)| = {res['weights'][idx]:7.3f}")
