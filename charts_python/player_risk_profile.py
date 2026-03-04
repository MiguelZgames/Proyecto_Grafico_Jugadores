import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_risk):
    if not p_risk:
        return go.Figure()
        
    x_vals = [d["amount_usd"] for d in p_risk]
    y_vals = [d["odds"] for d in p_risk]

    fig = go.Figure(go.Scattergl(
        x=x_vals, y=y_vals,
        mode='markers',
        marker=dict(color=paleta_corpo["royalBlue"], opacity=0.6, size=9, line=dict(color='#FFF', width=1)),
        hovertemplate='Monto: $%{x:,.2f}<br>Odds: %{y:.2f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        xaxis=dict(title='Monto (USD)'),
        yaxis=dict(title='Cuota')
    )
    fig.update_layout(**layout)
    return fig
