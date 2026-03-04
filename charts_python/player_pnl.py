import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_daily):
    if not p_daily:
        return go.Figure()

    x_vals = [d["date"] for d in p_daily]
    y_prof = [d["profit_usd"] for d in p_daily]
    y_dep = [d["deposits"] for d in p_daily]
    
    prof_colors = [paleta_corpo["emerald"] if y >= 0 else paleta_corpo["crimson"] for y in y_prof]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_vals, y=y_prof,
        name='Profit',
        marker=dict(color=prof_colors),
        hovertemplate='Profit: $%{y:,.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_dep,
        name='Depósitos',
        mode='lines+markers',
        line=dict(color=paleta_corpo["teal"], width=2, dash='dot'),
        hovertemplate='Dep: $%{y:,.2f}<extra></extra>'
    ))

    layout = get_base_layout()
    fig.update_layout(**layout)
    return fig
