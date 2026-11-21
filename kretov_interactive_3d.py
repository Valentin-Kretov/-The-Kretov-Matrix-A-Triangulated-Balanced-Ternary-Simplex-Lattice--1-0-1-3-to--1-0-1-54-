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
    ex, ey, ez = [], [], []
    for i in range(27):
        for j in range(i + 1, 27):
            if sum(abs(nodes[i][d] - nodes[j][d]) for d in range(3)) == 1:
                ex.extend([nodes[i][0], nodes[j][0], None])
                ey.extend([nodes[i][1], nodes[j][1], None])
                ez.extend([nodes[i][2], nodes[j][2], None])

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=ex, y=ey, z=ez, mode="lines",
        line=dict(color="rgba(120, 180, 255, 0.35)", width=3),
        hoverinfo="none", name="54 Tensegrity Edges"
    ))

    colors = {-1: "#FF595E", 0: "#8AC926", 1: "#1982C4"}
    names = {-1: "Layer I: Dynamics", 0: "Layer II: Substance", 1: "Layer III: Geometry"}
    for x_val in [-1, 0, 1]:
        pts = [n for n in nodes if n[0] == x_val and n != (0, 0, 0)]
        fig.add_trace(go.Scatter3d(
            x=[p[0] for p in pts], y=[p[1] for p in pts], z=[p[2] for p in pts],
            mode="markers", name=names[x_val],
            marker=dict(size=9, color=colors[x_val], line=dict(width=1.5, color="white")),
            text=[f"<b>{nodes_data[p][0]}</b><br>Value: {nodes_data[p][1]}<br>Node: {p}" for p in pts],
            hoverinfo="text"
        ))

    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0], mode="markers", name="Central Hub (0,0,0)",
        marker=dict(size=14, color="#FFFFFF", symbol="diamond", line=dict(width=2, color="#FFCA3A")),
        text=["<b>Central Focal Hub (0,0,0)</b><br>Zero-Point Attractor / Observer Focus"],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="The Kretov Matrix: 27 Nodes & 54 Tensegrity Edges",
        template="plotly_dark", margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(xaxis_title="X (Dynamics)", yaxis_title="Y (Substance)", zaxis_title="Z (Geometry)")
    )
    fig.write_html("kretov_matrix_3d_interactive.html", include_plotlyjs="cdn")


if __name__ == "__main__":
    build_interactive_matrix()
