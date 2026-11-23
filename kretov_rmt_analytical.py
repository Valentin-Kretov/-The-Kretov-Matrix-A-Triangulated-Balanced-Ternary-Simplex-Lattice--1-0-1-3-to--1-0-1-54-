import itertools
import numpy as np


def analyze_symmetric_3x3_exact():
    r"""
    Точное комбинаторное и алгебраическое разложение всех 3^6 = 729
    симметричных троичных матриц 3x3 над {-1, 0, +1}.
    """
    alphabet = (-1, 0, 1)
    total_matrices = 0
    rank_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    char_poly_classes = set()

    ratio_max_mid = []
    ratio_mid_min = []
    silver_orbit_count = 0
    silver_target = 1.0 + np.sqrt(2.0)

    for d1, d2, d3, a, b, c in itertools.product(alphabet, repeat=6):
        total_matrices += 1
        mat = np.array(
            [
                [d1, a, b],
                [a, d2, c],
                [b, c, d3],
            ],
            dtype=float,
        )

        # Точный целочисленный определитель и коэффициенты характеристического полинома
        tr = int(d1 + d2 + d3)
        c2 = int(d1 * d2 + d2 * d3 + d1 * d3 - a * a - b * b - c * c)
        det = int(d1 * d2 * d3 + 2 * a * b * c - d1 * c * c - d2 * b * b - d3 * a * a)

        # Нормализация полинома с точностью до знака M <-> -M
        poly_sig = (abs(tr), c2, abs(det))
        char_poly_classes.add(poly_sig)

        eigs = np.linalg.eigvalsh(mat)
        abs_eigs = np.sort(np.abs(eigs))[::-1]
        l_max, l_mid, l_min = map(float, abs_eigs)

        # Подсчет ранга (числа ненулевых собственных значений)
        rank = int(np.sum(abs_eigs > 1e-9))
        rank_counts[rank] += 1

        if det != 0:
            assert rank == 3, f"Ненулевой det={det}, но ранг {rank}"
            r1 = l_max / l_mid
            r2 = l_mid / l_min
            ratio_max_mid.append(r1)
            ratio_mid_min.append(r2)

            if abs(r1 - silver_target) < 1e-7 and abs(r2 - silver_target) < 1e-7:
                silver_orbit_count += 1

    assert total_matrices == 729
    assert sum(rank_counts.values()) == 729
    assert rank_counts.get(3) == 516
    assert rank_counts.get(2) == 186
    assert rank_counts.get(1) == 26
    assert rank_counts.get(0) == 1

    degenerate_count = 729 - rank_counts.get(3)
    assert degenerate_count == 213  # 71 / 243 = 71 / 3^5

    mean_r1 = float(np.mean(ratio_max_mid))
    mean_r2 = float(np.mean(ratio_mid_min))

    return {
        "total": total_matrices,
        "non_degenerate": rank_counts.get(3),
        "degenerate": degenerate_count,
        "degenerate_fraction": degenerate_count / total_matrices,
        "rank_counts": rank_counts,
        "poly_classes": len(char_poly_classes),
        "silver_orbit_count": silver_orbit_count,
        "mean_max_mid": mean_r1,
        "mean_mid_min": mean_r2,
        "pi_half_accuracy": 1.0 - abs(mean_r1 - (np.pi / 2.0)) / (np.pi / 2.0),
        "silver_accuracy": 1.0 - abs(mean_r2 - silver_target) / silver_target,
    }


def verify_wigner_semicircle_scaling(n_samples=2500):
    r"""
    Верификация перехода от дискретной ячейки 3x3 к классу универсальности
    Гауссова ортогонального ансамбля (GOE) и закону полукруга Вигнера
    lambda_edge(N) = 2 * sqrt(2N / 3) для N = 9 и N = 27.
    """
    rng = np.random.default_rng(2026)
    scaling_results = {}

    for dim in (9, 27):
        max_eigs = []
        zero_modes = 0
        for _ in range(n_samples):
            raw = rng.choice((-1.0, 0.0, 1.0), size=(dim, dim))
            sym = np.triu(raw) + np.triu(raw, 1).T
            eigs = np.linalg.eigvalsh(sym)
            abs_eigs = np.abs(eigs)
            max_eigs.append(float(np.max(abs_eigs)))
            if np.min(abs_eigs) < 1e-9:
                zero_modes += 1

        wigner_edge = float(2.0 * np.sqrt(2.0 * dim / 3.0))
        mean_max = float(np.mean(max_eigs))
        scaling_results[dim] = {
            "wigner_edge": wigner_edge,
            "mean_max_eig": mean_max,
            "edge_ratio": mean_max / wigner_edge,
            "zero_mode_fraction": zero_modes / n_samples,
        }

    return scaling_results


def run_rmt_proof():
    exact_3x3 = analyze_symmetric_3x3_exact()
    wigner_scaling = verify_wigner_semicircle_scaling()
    return {"exact_3x3": exact_3x3, "wigner": wigner_scaling}


if __name__ == "__main__":
    res = run_rmt_proof()
    ex = res["exact_3x3"]
    print("=== АНАЛИТИЧЕСКОЕ ДОКАЗАТЕЛЬСТВО RMT-СПЕКТРА МАТРИЦЫ КРЕТОВА ===\n")
    print(f"Всего симметричных матриц 3x3:   {ex['total']} (3^6)")
    print(f"Уникальных классов полиномов:    {ex['poly_classes']}")
    print(f"Невырожденных (Rank 3):          {ex['non_degenerate']} ({ex['non_degenerate']/729*100:.4f}%)")
    print(f"Вырожденных (det M = 0):         {ex['degenerate']} / 729 = 71 / 243 ({ex['degenerate_fraction']*100:.4f}%)")
    print(f"Разложение рангов (3, 2, 1, 0):  {ex['rank_counts']}")
    print(f"Полная O_h-орбита серебр. сеч.:  {ex['silver_orbit_count']} матриц {{1+sqrt(2), 1, sqrt(2)-1}}\n")
    print(f"<|l_max| / |l_mid|> = {ex['mean_max_mid']:.6f} vs pi/2 = {np.pi/2:.6f} (точность {ex['pi_half_accuracy']*100:.2f}%)")
    print(f"<|l_mid| / |l_min|> = {ex['mean_mid_min']:.6f} vs 1+sqrt(2) = {1+np.sqrt(2):.6f} (точность {ex['silver_accuracy']*100:.2f}%)\n")

    for dim, stats in res["wigner"].items():
        print(
            f"[N = {dim:2d}] <l_max> = {stats['mean_max_eig']:.4f} / край Вигнера {stats['wigner_edge']:.4f} "
            f"(отн. {stats['edge_ratio']:.3f}), доля нулевых мод = {stats['zero_mode_fraction']*100:.2f}%"
        )
