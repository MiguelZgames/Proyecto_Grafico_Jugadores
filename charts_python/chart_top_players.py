import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(df_top_players):
    if len(df_top_players) == 0:
        return go.Figure()
        
    df = df_top_players.sort("ggr_usd", descending=False)
    
    x_vals = df["ggr_usd"].to_list()
    y_vals = df["username"].to_list()

    text_vals = [f"${v:,.0f}" for v in x_vals]

    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_vals,
        orientation='h',
        marker=dict(
            color='#3B82F6',
            opacity=0.9,
            line=dict(width=1, color='white')
        ),
        text=text_vals,
        textposition='inside',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>Jugador:</b> %{y}<br>GGR: <b>$%{x:,.2f}</b><extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        height=380,
        margin=dict(t=10, b=20, l=120, r=20),
        yaxis=dict(showgrid=False, zeroline=False, automargin=True),
        xaxis=dict(showgrid=True, gridcolor='#F1F5F9', zeroline=False, tickformat='$,.0s'),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", color="#1F2937"))
    )
    fig.update_layout(**layout)
    return fig
