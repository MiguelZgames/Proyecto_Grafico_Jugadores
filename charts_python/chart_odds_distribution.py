import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(odds_hist):
    if not odds_hist or not odds_hist.get("bins"):
        return go.Figure()
        
    x_vals = odds_hist["bins"][:-1]
    y_vals = odds_hist["values"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_vals,
        y=y_vals,
        marker=dict(
            color=paleta_corpo.get("sky500", "#0EA5E9"),
            line=dict(color='white', width=1)
        ),
        opacity=0.9,
        hovertemplate="Cuota: <b>%{x:,.2f}</b><br>Frecuencia: <b>%{y:,.0f}</b><extra></extra>"
    ))

    layout = get_base_layout()
    layout.update(
        bargap=0.1,
        xaxis=dict(
            title="", 
            showgrid=False, 
            zeroline=False
        ),
        yaxis=dict(
            title="", 
            showgrid=False, 
            gridcolor="#F1F5F9", 
            zeroline=False, 
            showline=False
        ),
        margin=dict(l=40, r=20, t=30, b=40),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(family="Inter", color="#1F2937")
        )
    )
    fig.update_layout(**layout)
    return fig
