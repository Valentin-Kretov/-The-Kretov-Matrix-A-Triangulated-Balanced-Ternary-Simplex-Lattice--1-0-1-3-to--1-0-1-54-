import itertools
import numpy as np
from fractions import Fraction


def run_exact_combinatorial_audit():
    print("=== EXACT COMBINATORIAL AUDIT OF TERNARY 3x3 OPERATORS ===")
    alphabet = [-1, 0, 1]

    # 1. All 3^9 = 19,683 general ternary 3x3 matrices
    total_all = 3**9
    zero_det_all = 0
    zero_det_wigner = 0
    radii_wigner = []

    for entries in itertools.product(alphabet, repeat=9):
        m = np.array(entries, dtype=float).reshape(3, 3)
        if abs(np.linalg.det(m)) < 1e-9:
            zero_det_all += 1

        m_wig = 0.5 * (m + m.T)
        if abs(np.linalg.det(m_wig)) < 1e-9:
            zero_det_wigner += 1
        radii_wigner.append(np.max(np.abs(np.linalg.eigvalsh(m_wig))))

    frac_all = Fraction(zero_det_all, total_all)
    frac_wig = Fraction(zero_det_wigner, total_all)

    # 2. Direct symmetric ternary 3x3 matrices (3^6 = 729)
    total_sym = 3**6
    zero_det_sym = 0
    radii_sym = []

    for d0, d1, d2, a01, a02, a12 in itertools.product(alphabet, repeat=6):
        m_sym = np.array([
            [d0, a01, a02],
            [a01, d1, a12],
            [a02, a12, d2],
        ], dtype=float)
        if abs(np.linalg.det(m_sym)) < 1e-9:
            zero_det_sym += 1
        radii_sym.append(np.max(np.abs(np.linalg.eigvalsh(m_sym))))

    frac_sym = Fraction(zero_det_sym, total_sym)
    mean_rad_sym = float(np.mean(radii_sym))
    norm_rad_sym = mean_rad_sym * np.sqrt(8.0 / 3.0)

    print(f"General 3x3 (N={total_all}): det=0 -> {frac_all} ({float(frac_all)*100:.6f}%)")
    print(f"Direct Symmetric 3x3 (N={total_sym}): det=0 -> {frac_sym} ({float(frac_sym)*100:.6f}%)")
    print(f"Direct Symmetric Mean Radius: {mean_rad_sym:.6f} | 4D-Normalized: {norm_rad_sym:.6f}")
    print(f"Wigner Symmetric (A+A^T)/2 (N={total_all}): det=0 -> {frac_wig} ({float(frac_wig)*100:.6f}%)")


if __name__ == "__main__":
    run_exact_combinatorial_audit()
