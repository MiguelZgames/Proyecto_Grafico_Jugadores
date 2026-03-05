import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_house_risk):
    if not df_house_risk or len(df_house_risk) == 0:
        return go.Figure()

    x_vals = [d["type_bet"] for d in df_house_risk]
    y_vals = [d["profit"] for d in df_house_risk]
    colors = [paleta_corpo["emerald"] if v >= 0 else paleta_corpo["crimson"] for v in y_vals]

    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_vals,
        marker=dict(color=colors, opacity=0.9, line=dict(width=1, color='white')),
        hovertemplate='<b>%{x}</b><br>House Profit: <b>$%{y:,.0f}</b><extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        yaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#94A3B8"),
        xaxis=dict(title="", showgrid=False),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", color="#1F2937"))
    )
    fig.update_layout(**layout)
    return fig
