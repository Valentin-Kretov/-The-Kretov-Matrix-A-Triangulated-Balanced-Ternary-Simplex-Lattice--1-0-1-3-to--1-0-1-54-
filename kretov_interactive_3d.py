import itertools
import plotly.graph_objects as go


def build_interactive_matrix():
    # Словарь из 27 узлов с физическими константами и параметрами (полный код доступен в исходных материалах)
    nodes_data = {
        (-1, -1, -1): ("Weak Mixing Angle (sin²θ_W)", "0.2312", "Layer I: Dynamics"),
        # ... (полная структура включает все 27 узлов от Layer I до Layer III и центральный аттрактор)
        (0, 0, 0): ("27th Constant: Strong CP (θ_QCD)", "0 (Focal Attractor)", "Central Hub (0,0,0)"),
        # ...
    }
    # Логика построения сетки, рёбер тенсегрити и визуализации в Plotly
    nodes = list(itertools.product([-1, 0, 1], repeat=3))
    # ...
    fig = go.Figure()
    # Настройка слоев, центрального маркера и параметров сцены
    # ...
    fig.write_html("kretov_matrix_3d_interactive.html", include_plotlyjs="cdn")
    print("Interactive 3D HTML generated successfully.")


if __name__ == "__main__":
    build_interactive_matrix()
