import itertools
import numpy as np
import matplotlib.pyplot as plt

def run_7d_scaling_audit():
    kernel = np.ones(3, dtype=int)
    for n in range(8):
        if n == 0:
            z = 1
        else:
            poly = np.ones(1, dtype=int)
            for _ in range(n):
                poly = np.convolve(poly, kernel)
            z = poly[n]
        print(f"3^{n} = {3**n:4d} | Q=0: {z:3d} | sigma={np.sqrt(2.0*n/3.0):.4f}")

def generate_7d_petrie_rosette():
    dim = 7
    nodes = np.array(list(itertools.product([-1, 0, 1], repeat=dim)))
    charges = np.sum(nodes, axis=1)
    angles = np.array([np.pi * k / dim for k in range(dim)])
    proj_x = nodes @ np.cos(angles)
    proj_y = nodes @ np.sin(angles)

    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#0b0f19")
    ax.set_facecolor("#0b0f19")
    scatter = ax.scatter(proj_x, proj_y, c=charges, cmap="coolwarm", s=28, alpha=0.82, edgecolors="none", zorder=3)
    ax.scatter((0,), (0,), color="gold", s=220, edgecolors="white", linewidth=1.5, zorder=5, label="Central Equilibrium (0^7)")
    cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Net Topological Charge Q", color="white", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")
    ax.set_title("The Kretov Matrix (3^7 = 2,187 States): 14-Fold Petrie Rosette Projection", color="white", fontsize=13, pad=16)
    ax.axis("off")
    ax.legend(loc="upper right", facecolor="#161b22", edgecolor="gray", labelcolor="white", fontsize=9)
    plt.tight_layout()
    plt.savefig("kretov_7d_rosette.png", dpi=300, facecolor=fig.get_facecolor())
    print("Saved kretov_7d_rosette.png")

if __name__ == "__main__":
    run_7d_scaling_audit()
    generate_7d_petrie_rosette()
