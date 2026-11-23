import numpy as np


def get_26_dimensionless_constants():
    r"""
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
        "theta23_PMNS": np.deg2rad(45.00),
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

    assert len(constants) == 26
    assert all(val > 0 for val in constants.values())
    return constants


def generate_lattice_nodes():
    r"""
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
    for x, y, z in nodes:
        v = (x, y, z)
        anti_v = (-x, -y, -z)
        assert anti_v in node_set
        if v not in visited:
            pairs.append((v, anti_v))
            visited.add(v)
            visited.add(anti_v)

    assert len(pairs) == 13
    return np.array(nodes, dtype=float), pairs


def compute_pairwise_compensation(constants):
    r"""
    Вариант 1: Аналитический поиск глобального минимума попарной компенсации
    w_a + w_b -> const, где w_i = |ln(X_i)|.
    """
    items = sorted([(k, float(abs(np.log(v)))) for k, v in constants.items()], key=lambda pair: pair)
    weights = np.array([w for _, w in items])
    target = float(2.0 * np.mean(weights))

    pairs_out = []
    sums = []
    for k in range(13):
        na, wa = items[k]
        nb, wb = items[25 - k]
        s = wa + wb
        sums.append(s)
        pairs_out.append((na, nb, wa, wb, s))

    sums_arr = np.array(sums)
    cv = float(np.std(sums_arr) / np.mean(sums_arr))
    return pairs_out, target, cv


def search_3d_equilibrium(weights, nodes, layer_groups=None, n_restarts=6, steps=35_000):
    r"""
    Быстрый инкрементальный поиск глобального 3D-равновесия
    (дипольный момент -> min и изотропия тензора инерции).
    """
    n = len(weights)
    total_w = float(np.sum(weights))
    nx, ny, nz = nodes[:, 0], nodes[:, 1], nodes[:, 2]

    # Предвычисленные геометрические коэффициенты для каждого узла
    g_xx = ny ** 2 + nz ** 2
    g_yy = nx ** 2 + nz ** 2
    g_zz = nx ** 2 + ny ** 2
    g_xy = -nx * ny
    g_xz = -nx * nz
    g_yz = -ny * nz

    def full_eval(perm):
        w = weights[perm]
        dip = np.sum(w[:, None] * nodes, axis=0)
        I_vec = np.array([
            np.sum(w * g_xx), np.sum(w * g_yy), np.sum(w * g_zz),
            np.sum(w * g_xy), np.sum(w * g_xz), np.sum(w * g_yz)
        ])
        return dip, I_vec

    def loss_from_state(dip, I_vec):
        dip_err = float(np.linalg.norm(dip) / total_w)
        I_xx, I_yy, I_zz, I_xy, I_xz, I_yz = I_vec
        diag_mean = (I_xx + I_yy + I_zz) / 3.0
        aniso = float((np.std([I_xx, I_yy, I_zz]) + abs(I_xy) + abs(I_xz) + abs(I_yz)) / diag_mean)
        return dip_err + 0.1 * aniso, dip_err, aniso

    best_loss = float("inf")
    best_state = None

    for run in range(n_restarts):
        rng = np.random.default_rng(2026 + run)
        perm = np.zeros(n, dtype=int)

        if layer_groups is not None:
            for n_grp, c_grp in layer_groups:
                perm[n_grp] = rng.permutation(c_grp)
        else:
            perm = rng.permutation(n)

        dip, I_vec = full_eval(perm)
        curr_loss, curr_dip, curr_aniso = loss_from_state(dip, I_vec)

        for step in range(steps):
            T = 0.02 * ((1e-6 / 0.02) ** (step / steps))
            if layer_groups is not None:
                g_idx = int(rng.integers(0, len(layer_groups)))
                grp = layer_groups[g_idx]
                i, j = rng.choice(grp, size=2, replace=False)
            else:
                i, j = rng.choice(n, size=2, replace=False)

            wi, wj = weights[perm[i]], weights[perm[j]]
            dw = wj - wi

            # Инкрементальное обновление O(1) без пересчета всего массива
            new_dip = dip + dw * (nodes[i] - nodes[j])
            dI = np.array([
                dw * (g_xx[i] - g_xx[j]),
                dw * (g_yy[i] - g_yy[j]),
                dw * (g_zz[i] - g_zz[j]),
                dw * (g_xy[i] - g_xy[j]),
                dw * (g_xz[i] - g_xz[j]),
                dw * (g_yz[i] - g_yz[j]),
            ])
            new_I = I_vec + dI
            new_loss, new_dip_err, new_aniso = loss_from_state(new_dip, new_I)

            if new_loss < curr_loss or rng.random() < np.exp((curr_loss - new_loss) / T):
                perm[i], perm[j] = perm[j], perm[i]
                dip, I_vec = new_dip, new_I
                curr_loss, curr_dip, curr_aniso = new_loss, new_dip_err, new_aniso
                if new_loss < best_loss:
                    best_loss = new_loss
                    best_state = (perm.copy(), new_dip_err, new_aniso, new_dip.copy())

    best_perm, best_dip, best_aniso, best_vec = best_state
    assert len(set(best_perm)) == n
    return best_perm, best_dip, best_aniso, best_vec


def compute_pvalue(weights, nodes, target_dip_err, n_samples=2000):
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
    nodes, pairs = generate_lattice_nodes()
    names = list(constants.keys())
    weights = np.array([float(abs(np.log(constants[k]))) for k in names])

    pairs_out, target_s, cv_1 = compute_pairwise_compensation(constants)

    # 1. Полный 26-базис (СМ + космологическая постоянная Lambda)
    perm_26, dip_26, aniso_26, vec_26 = search_3d_equilibrium(weights, nodes)
    p_26 = compute_pvalue(weights, nodes, dip_26)

    # 2. Чистый квантовый 25-базис СМ (без вакуумной энергии Lambda)
    # Исключаем Lambda_dimless и противоположный ей полярный узел (-1,-1,-1)
    sm_indices = [i for i, k in enumerate(names) if k != "Lambda_dimless"]
    sm_weights = weights[sm_indices]
    sm_nodes = nodes[1:]  # 25 узлов без (-1,-1,-1)
    perm_25, dip_25, aniso_25, vec_25 = search_3d_equilibrium(sm_weights, sm_nodes)
    p_25 = compute_pvalue(sm_weights, sm_nodes, dip_25)

    return {
        "pairwise_cv": cv_1,
        "pairwise_target": target_s,
        "pairs": pairs_out,
        "free_dip_err": dip_26,
        "free_aniso": aniso_26,
        "free_vec": vec_26,
        "free_perm": perm_26,
        "free_pvalue": p_26,
        "sm25_dip_err": dip_25,
        "sm25_aniso": aniso_25,
        "sm25_vec": vec_25,
        "sm25_pvalue": p_25,
        "names": names,
        "weights": weights,
        "nodes": nodes,
    }


if __name__ == "__main__":
    res = run_full_audit()
    print("=== АУДИТ ЦЕНТРАЛЬНОГО РАВНОВЕСИЯ МАТРИЦЫ КРЕТОВА ===\n")
    print(f"[Вариант 1] Попарная компенсация: средняя сумма = {res['pairwise_target']:.3f}, разброс = {res['pairwise_cv']*100:.2f}%\n")
    print(f"[Вариант 2A: Полный 26-базис СМ + Lambda]")
    print(f"  Вакуумный остаток (движущая сила Lambda): {res['free_dip_err']*100:.4f}% (p={res['free_pvalue']:.5f})")
    print(f"  Анизотропия тензора инерции:              {res['free_aniso']:.6e}\n")
    print(f"[Вариант 2B: Чистый 25-базис СМ без Lambda]")
    print(f"  Остаточный квантовый диполь:              {res['sm25_dip_err']*100:.6f}% (p={res['sm25_pvalue']:.5f})\n")
    print("Карта 26 узлов:")
    for node, idx in zip(res["nodes"], res["free_perm"]):
        x, y, z = map(int, node)
        print(f"  ({x:+d},{y:+d},{z:+d}) -> {res['names'][idx]:<15} | |ln(X)| = {res['weights'][idx]:7.3f}")
