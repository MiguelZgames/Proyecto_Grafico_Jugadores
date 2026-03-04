import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()
        
    x_vals = df_segments["group_name"].to_list()
    y_ggr = df_segments["ggr_usd"].to_list()
    y_dep = df_segments["deposits"].to_list()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_vals, y=y_ggr,
        name='GGR',
        marker=dict(color=paleta_corpo["emerald"], line=dict(width=0)),
        hovertemplate='GGR: $%{y:,.0f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=x_vals, y=y_dep,
        name='Depósitos',
        marker=dict(color=paleta_corpo["teal"], line=dict(width=0)),
        hovertemplate='Depósitos: $%{y:,.0f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(barmode='group')
    fig.update_layout(**layout)
    return fig
