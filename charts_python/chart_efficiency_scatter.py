import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()
        
    x_vals = df_segments["deposits"].to_list()
    y_vals = df_segments["ggr_usd"].to_list()
    text_vals = df_segments["group_name"].to_list()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
              '#393b79', '#5254a3', '#6b6ecf', '#9c9ede', '#637939']
              
    sc_colors = [colors[i % 15] for i in range(len(x_vals))]

    fig = go.Figure(go.Scatter(
        x=x_vals, y=y_vals,
        mode='markers+text',
        text=text_vals,
        textposition='top center',
        marker=dict(size=18, color=sc_colors, opacity=0.8, line=dict(width=0)),
        hovertemplate='<b>Depósitos:</b> $%{x:,.0f}<br><b>GGR:</b> $%{y:,.0f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='', showgrid=True, gridcolor='#F1F5F9')
    )
    fig.update_layout(**layout)
    return fig
