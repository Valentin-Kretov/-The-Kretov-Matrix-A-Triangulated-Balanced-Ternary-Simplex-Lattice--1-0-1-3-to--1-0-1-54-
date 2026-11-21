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
    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    # Проекция в триангулированную симплекс-пирамиду (углы 60/120 градусов)
    # Координаты 9 узлов в виде вложенного равностороннего треугольника
    tri_2d = {
        (-1, -1): ( 0.00,  1.15),   # Верхняя вершина треугольника
        ( 1, -1): (-1.00, -0.58),   # Левая нижняя вершина
        ( 1,  1): ( 1.00, -0.58),   # Правая нижняя вершина
        ( 0, -1): (-0.50,  0.29),   # Середина левой стороны
        ( 0,  0): ( 0.50,  0.29),   # Середина правой стороны
        ( 1,  0): ( 0.00, -0.58),   # Середина нижней стороны
        (-1,  0): (-0.28,  0.16),   # Внутренний левый узел
        (-1,  1): ( 0.28,  0.16),   # Внутренний правый узел
        ( 0,  1): ( 0.00, -0.15),   # Центр треугольного слоя
    }

    def to_pyramid(x, y, z):
        # Слой I (-1) — широкое основание, Слой II (0) — середина, Слой III (+1) — вершина
        scale = { -1: 1.35, 0: 0.95, 1: 0.58 }[x]
        bx, by = tri_2d[(y, z)]
        return (bx * scale, by * scale, x * 1.4)

    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    pos = {n: to_pyramid(*n) for n in nodes}

    # Строим 54 ребра: 18 треугольных ребер внутри каждого слоя + вертикальные связи
    ex, ey, ez = [], [], []
    layer_edges = [
        ((-1, -1), (0, -1)), ((0, -1), (1, -1)),   # Левая сторона
        ((-1, -1), (0,  0)), ((0,  0), (1,  1)),   # Правая сторона
        (( 1, -1), (1,  0)), ((1,  0), (1,  1)),   # Нижняя сторона
        (( 0, -1), (0,  0)), ((0,  0), (1,  0)), ((1, 0), (0, -1)), # Срединный треугольник
        ((-1, -1), (-1, 0)), ((-1, -1), (-1, 1)),  # Внутренние лучи к вершине
        (( 1, -1), (-1, 0)), (( 1,  1), (-1, 1)),
        ((-1,  0), (-1, 1)), ((-1,  0), ( 0, 1)), ((-1, 1), (0, 1)), ((1, 0), (0, 1)), ((0, 0), (0, 1))
    ]

    for x_val in [-1, 0, 1]:
        for u, v in layer_edges:
            p1, p2 = pos[(x_val, u[0], u[1])], pos[(x_val, v[0], v[1])]
            ex.extend([p1[0], p2[0], None])
            ey.extend([p1[1], p2[1], None])
            ez.extend([p1[2], p2[2], None])

    # Вертикальные связи между тремя треугольными слоями
    for yz in tri_2d:
        for x1, x2 in [(-1, 0), (0, 1)]:
            p1, p2 = pos[(x1, yz[0], yz[1])], pos[(x2, yz[0], yz[1])]
            ex.extend([p1[0], p2[0], None])
            ey.extend([p1[1], p2[1], None])
            ez.extend([p1[2], p2[2], None])

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=ex, y=ey, z=ez, mode="lines",
        line=dict(color="rgba(100, 200, 255, 0.45)", width=2.5),
        hoverinfo="none", name="54 Tensegrity Edges"
    ))

    colors = {-1: "#FF595E", 0: "#8AC926", 1: "#1982C4"}
    names = {-1: "Layer I: Dynamics (Base)", 0: "Layer II: Substance (Core)", 1: "Layer III: Geometry (Apex)"}
    for x_val in [-1, 0, 1]:
        pts = [n for n in nodes if n[0] == x_val and n != (0, 0, 0)]
        fig.add_trace(go.Scatter3d(
            x=[pos[p][0] for p in pts],
            y=[pos[p][1] for p in pts],
            z=[pos[p][2] for p in pts],
            mode="markers+text", name=names[x_val],
            marker=dict(size=8, color=colors[x_val], line=dict(width=1.5, color="white")),
            text=[nodes_data[p][0].split("(")[-1].rstrip(")") for p in pts],
            textposition="top center",
            textfont=dict(size=9, color="rgba(255,255,255,0.9)"),
            hovertext=[f"<b>{nodes_data[p][0]}</b><br>Value: {nodes_data[p][1]}<br>Coord: {p}" for p in pts],
            hoverinfo="text"
        ))

    cx, cy, cz = pos[(0, 0, 0)]
    fig.add_trace(go.Scatter3d(
        x=[cx], y=[cy], z=[cz], mode="markers+text", name="27th Node: Focal Hub (0,0,0)",
        marker=dict(size=14, color="#FFFFFF", symbol="diamond", line=dict(width=2, color="#FFCA3A")),
        text=["θ_QCD = 0"], textposition="bottom center",
        textfont=dict(size=11, color="#FFCA3A"),
        hovertext=["<b>Central Focal Hub (0,0,0)</b><br>Strong CP = 0 / Observer Focus"],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="The Kretov Matrix: Triangulated Balanced Ternary Simplex Pyramid",
        template="plotly_dark", margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.1))
        )
    )
    fig.write_html("kretov_matrix_3d_interactive.html", include_plotlyjs="cdn")


if __name__ == "__main__":
    build_interactive_matrix()
