import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_turnover):
    if not p_turnover:
        return go.Figure()
        
    tot_dep = p_turnover.get("deposits", 0)
    tot_apo = p_turnover.get("amount_usd", 0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[tot_dep], y=['Métricas'], name='Depósitos',
        orientation='h', marker=dict(color=paleta_corpo["teal"]),
        hovertemplate='$%{x:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=[tot_apo], y=['Métricas'], name='Apostado',
        orientation='h', marker=dict(color=paleta_corpo["royalBlue"]),
        hovertemplate='$%{x:,.0f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        barmode='group',
        margin=dict(l=70, r=10, t=10, b=40)
    )
    fig.update_layout(**layout)
    return fig
