import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(odds_hist):
    if not odds_hist or not odds_hist.get("bins"):
        return go.Figure()
        
    x_vals = odds_hist["bins"][:-1]
    y_vals = odds_hist["values"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_vals, y=y_vals,
        marker=dict(color=paleta_corpo["sky500"], line=dict(width=0)),
        opacity=0.9,
        hovertemplate='<b>Frecuencia:</b> %{y:.4f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        yaxis=dict(title='', showgrid=True, gridcolor='#F1F5F9', zeroline=False, showline=False)
    )
    fig.update_layout(**layout)
    return fig
