import numpy as np

def run_triangulated_precision_solver():
    base, cycle_6, stratum_9 = 3, 3**6, 3**2
    data = [
        ("alpha^-1", (4*np.pi**3 + np.pi**2 + np.pi) - (base / (4.0*np.pi*cycle_6)), 137.035999),
        ("sin^2 theta_W", (base / 13.0) + (1.0 / (base*cycle_6)), 0.231220),
        ("alpha_s", (1.0 / (6.0*np.sqrt(2.0))) * (1.0 + 1.0/cycle_6), 0.118000),
        ("theta_12 CKM (deg)", np.rad2deg(np.arcsin(1.0/np.sqrt(20.0)) + (base / (2.0*cycle_6))), 13.040000),
        ("theta_12 PMNS (deg)", np.rad2deg(np.arcsin(np.sqrt((1.0/base) - (1.0 / (2.0*stratum_9*np.sqrt(base)))))), 33.410000),
    ]
    for name, calc, exp in data:
        acc = (1.0 - abs(calc - exp) / exp) * 100
        print(f"{name:<20} | Calc: {calc:<10.6f} | Exp: {exp:<10.6f} | Acc: {acc:.5f}%")

if __name__ == "__main__":
    run_triangulated_precision_solver()
