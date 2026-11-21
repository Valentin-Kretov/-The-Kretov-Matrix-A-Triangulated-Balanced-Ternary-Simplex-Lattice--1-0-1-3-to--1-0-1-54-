import itertools
import plotly.graph_objects as go


def build_interactive_matrix():
    nodes_data = {
        (-1, -1, -1): ("Weak Mixing Angle (sin2_thetaW)", "0.2312", "Layer I: Dynamics"),
        (-1, -1,  0): ("Fine-Structure Constant (alpha)", "1/137.036", "Layer I: Dynamics"),
        (-1, -1,  1): ("Strong Coupling (alpha_s)", "0.1180", "Layer I: Dynamics"),
        (-1,  0, -1): ("Higgs VEV (v)", "246.22 GeV", "Layer I: Dynamics"),
        (-1,  0,  0): ("Higgs Boson Mass (m_H)", "125.10 GeV", "Layer I: Dynamics"),
        (-1,  0,  1): ("Cosmological Constant (Lambda)", "10^-122 M_Pl^4", "Layer I: Dynamics"),
        (-1,  1, -1): ("Quark CP Phase (delta_CKM)", "68 deg", "Layer I: Dynamics"),
        (-1,  1,  0): ("27th Constant: Strong CP (theta_QCD)", "0 (Equilibrium)", "Layer I: Dynamics"),
        (-1,  1,  1): ("Lepton CP Phase (delta_PMNS)", "195 deg", "Layer I: Dynamics"),
        ( 0, -1, -1): ("Up Quark (m_u)", "2.16 MeV", "Layer II: Substance"),
        ( 0, -1,  0): ("Charm Quark (m_c)", "1.27 GeV", "Layer II: Substance"),
        ( 0, -1,  1): ("Top Quark (m_t)", "172.7 GeV", "Layer II: Substance"),
        ( 0,  0, -1): ("Down Quark (m_d)", "4.67 MeV", "Layer II: Substance"),
        ( 0,  0,  0): ("Central Focal Hub (0,0,0)", "Zero-Point Attractor", "Layer II: Core"),
        ( 0,  0,  1): ("Bottom Quark (m_b)", "4.18 GeV", "Layer II: Substance"),
        ( 0,  1, -1): ("Electron (m_e)", "0.511 MeV", "Layer II: Substance"),
        ( 0,  1,  0): ("Muon (m_mu)", "105.66 MeV", "Layer II: Substance"),
        ( 0,  1,  1): ("Tau Lepton (m_tau)", "1776.86 MeV", "Layer II: Substance"),
        ( 1, -1, -1): ("Neutrino m_1", "0.36 meV (Predicted)", "Layer III: Geometry"),
        ( 1, -1,  0): ("Neutrino m_2", "8.62 meV (Predicted)", "Layer III: Geometry"),
        ( 1, -1,  1): ("Neutrino m_3", "50.15 meV (Predicted)", "Layer III: Geometry"),
        ( 1,  0, -1): ("Cabibbo Angle (theta_12^CKM)", "13.04 deg", "Layer III: Geometry"),
        ( 1,  0,  0): ("Quark Mixing (theta_23^CKM)", "2.38 deg", "Layer III: Geometry"),
        ( 1,  0,  1): ("Quark Mixing (theta_13^CKM)", "0.20 deg", "Layer III: Geometry"),
        ( 1,  1, -1): ("Solar Angle (theta_12^PMNS)", "33.41 deg", "Layer III: Geometry"),
        ( 1,  1,  0): ("Atmospheric Angle (theta_23^PMNS)", "45.00 deg", "Layer III: Geometry"),
        ( 1,  1,  1): ("Reactor Angle (theta_13^PMNS)", "8.54 deg", "Layer III: Geometry"),
    }
    def to_merkaba(x, y, z):
        # Прямое симплексное преобразование куба {-1,0,+1}^3 в Звёздчатый октаэдр (Меркабу):
        # 8 углов (±1,±1,±1) образуют два встречных тетраэдра (+1 вверх и -1 вниз)
        import math
        # Поворот вдоль главной диагонали (1,1,1) так, чтобы (1,1,1) смотрел строго вверх (+Z),
        # а (-1,-1,-1) — строго вниз (-Z)
        px = (x - y) / math.sqrt(2.0)
        py = (x + y - 2.0 * z) / math.sqrt(6.0)
        pz = (x + y + z) / math.sqrt(3.0)

        # Усиливаем вытяжку 8 полярных вершин (±1,±1,±1), чтобы четко проявились лучи Меркабы
        if abs(x) == 1 and abs(y) == 1 and abs(z) == 1:
            px *= 1.35
            py *= 1.35
            pz *= 1.35
        return (px, py, pz)

    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    pos = {n: to_merkaba(*n) for n in nodes}

    ex, ey, ez = [], [], []
    for i in range(27):
        for j in range(i + 1, 27):
            nx1, ny1, nz1 = nodes[i]
            nx2, ny2, nz2 = nodes[j]
            dx, dy, dz = nx2 - nx1, ny2 - ny1, nz2 - nz1
            manhattan = abs(dx) + abs(dy) + abs(dz)
            if manhattan == 1:
                x1, y1, z1 = pos[nodes[i]]
                x2, y2, z2 = pos[nodes[j]]
                ex.extend([x1, x2, None])
                ey.extend([y1, y2, None])
                ez.extend([z1, z2, None])

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=ex, y=ey, z=ez, mode="lines",
        line=dict(color="rgba(110, 210, 255, 0.45)", width=2.5),
        hoverinfo="none", name="54 Tensegrity Star Edges"
    ))

    colors = {-1: "#FF595E", 0: "#8AC926", 1: "#1982C4"}
    names = {-1: "Layer I: Dynamics (-1)", 0: "Layer II: Substance (0)", 1: "Layer III: Geometry (+1)"}
    for x_val in (-1, 0, 1):
        pts = [n for n in nodes if n[0] == x_val and n != (0, 0, 0)]
        px_list = [pos[p][0] for p in pts]
        py_list = [pos[p][1] for p in pts]
        pz_list = [pos[p][2] for p in pts]
        labels = [nodes_data[p][0].split("(")[-1].rstrip(")") for p in pts]
        hovers = [f"<b>{nodes_data[p][0]}</b><br>Value: {nodes_data[p][1]}<br>Coord: {p}" for p in pts]

        fig.add_trace(go.Scatter3d(
            x=px_list, y=py_list, z=pz_list,
            mode="markers+text", name=names[x_val],
            marker=dict(size=8, color=colors[x_val], line=dict(width=1.5, color="white")),
            text=labels, textposition="top center",
            textfont=dict(size=9, color="rgba(255,255,255,0.9)"),
            hovertext=hovers, hoverinfo="text"
        ))

    cx, cy, cz = pos[(0, 0, 0)]
    fig.add_trace(go.Scatter3d(
        x=[cx], y=[cy], z=[cz], mode="markers+text", name="27th Node: Focal Hub (0,0,0)",
        marker=dict(size=15, color="#FFFFFF", symbol="diamond", line=dict(width=2.5, color="#FFCA3A")),
        text=["θ_QCD = 0 (HUB)"], textposition="bottom center",
        textfont=dict(size=11, color="#FFCA3A"),
        hovertext=["<b>Central Focal Hub (0,0,0)</b><br>Strong CP = 0 / Observer Focus"],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="The Kretov Matrix: Triangulated Balanced Ternary Star Simplex",
        template="plotly_dark", margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            camera=dict(eye=dict(x=0.0, y=-0.1, z=2.3))
        )
    )
    fig.write_html("kretov_matrix_3d_interactive.html", include_plotlyjs="cdn")


if __name__ == "__main__":
    build_interactive_matrix()
