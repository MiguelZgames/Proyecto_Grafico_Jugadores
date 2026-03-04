import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_top_players):
    if len(df_top_players) == 0:
        return go.Figure()
        
    df = df_top_players.sort("ggr_usd", descending=False)
    
    x_vals = df["ggr_usd"].to_list()
    y_vals = df["username"].to_list()

    fig = go.Figure(go.Bar(
        x=x_vals, y=y_vals,
        orientation='h',
        marker=dict(color='#3B82F6', line=dict(width=0)),
        hovertemplate='<b>GGR:</b> $%{x:,.2f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        margin=dict(t=0, b=20, l=100, r=10),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis=dict(showgrid=True, gridcolor='#F1F5F9', zeroline=False)
    )
    fig.update_layout(**layout)
    return fig
