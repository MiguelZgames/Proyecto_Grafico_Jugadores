import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_turnover):
    if not p_turnover:
        return go.Figure()

    tot_dep = p_turnover.get("deposits", 0)
    tot_apo = p_turnover.get("amount_usd", 0)
    ratio = tot_apo / tot_dep if tot_dep > 0 else 0

    fig = go.Figure()

    # Apostado (primero, barra más larga)
    fig.add_trace(go.Bar(
        x=[tot_apo], y=['Apostado'], name='Apostado',
        orientation='h', marker=dict(color=paleta_corpo["royalBlue"], cornerradius=4),
        text=[f'${tot_apo:,.0f}'], textposition='inside', textfont=dict(color='white', size=13, family='Inter'),
        hovertemplate="<b>Volumen Apostado</b><br>Dinero total utilizado en apuestas<br><b>$%{x:,.0f}</b><extra></extra>"
    ))

    # Depósitos (segundo, barra más corta)
    fig.add_trace(go.Bar(
        x=[tot_dep], y=['Depósitos'], name='Depósitos',
        orientation='h', marker=dict(color=paleta_corpo["teal"], cornerradius=4),
        text=[f'${tot_dep:,.0f}'], textposition='inside', textfont=dict(color='white', size=13, family='Inter'),
        hovertemplate="<b>Depósitos Totales</b><br>Dinero total depositado en la plataforma<br><b>$%{x:,.0f}</b><extra></extra>"
    ))

    ratio_text = f"Turnover: {ratio:.1f}x"
    insight = f"Cada dólar depositado se apuesta ~{ratio:.1f} veces"

    layout = get_base_layout()
    layout.update(
        autosize=True, height=280,
        barmode='group', bargap=0.35,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False, automargin=True,
                   tickfont=dict(size=12, color='#475569', family='Inter')),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0",
                        font=dict(family="Inter", size=12, color="#1F2937")),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center',
                    font=dict(size=11, color='#64748b')),
        annotations=[
            dict(
                x=0.98, y=1.12, xref='paper', yref='paper',
                text=f"<b>{ratio_text}</b>",
                showarrow=False, font=dict(size=18, color=paleta_corpo["royalBlue"], family='Inter'),
                xanchor='right'
            ),
            dict(
                x=0.5, y=-0.12, xref='paper', yref='paper',
                text=f"<i>{insight}</i>",
                showarrow=False, font=dict(size=11, color='#94A3B8', family='Inter'),
                xanchor='center'
            )
        ]
    )
    fig.update_layout(**layout)
    return fig
