import plotly.graph_objects as go
from charts_python.utils import PRIMARY_COLOR, NEUTRAL_COLOR, get_base_layout

def build_chart(player_turnover_data):
    if not player_turnover_data:
        return go.Figure()

    # Data preparation & Derived metrics
    total_deposits = player_turnover_data.get("deposits", 0)
    total_bet_amount = player_turnover_data.get("amount_usd", 0)
    
    turnover_ratio = (total_bet_amount / total_deposits) if total_deposits > 0 else 0

    # Chart traces
    figure_object = go.Figure()

    # Apostado (Volumen apostado explícitamente es Slate Blue por las reglas)
    bar_amount_bet = go.Bar(
        x=[total_bet_amount], 
        y=['Apostado'], 
        name='Apostado',
        orientation='h', 
        marker=dict(color="#334155", cornerradius=4),
        text=[f'${total_bet_amount:,.0f}'], 
        textposition='inside', 
        textfont=dict(color='white', size=13, family='Inter'),
        hovertemplate="<b>Volumen Apostado</b><br>Dinero total utilizado en apuestas<br><b>$%{x:,.0f}</b><extra></extra>"
    )
    figure_object.add_trace(bar_amount_bet)

    # Depósitos (Referencia Principal de capital)
    bar_amount_deposits = go.Bar(
        x=[total_deposits], 
        y=['Depósitos'], 
        name='Depósitos',
        orientation='h', 
        marker=dict(color="#1E3A8A", cornerradius=4),
        text=[f'${total_deposits:,.0f}'], 
        textposition='inside', 
        textfont=dict(color='white', size=13, family='Inter'),
        hovertemplate="<b>Depósitos Totales</b><br>Dinero total depositado en la plataforma<br><b>$%{x:,.0f}</b><extra></extra>"
    )
    figure_object.add_trace(bar_amount_deposits)

    # Layout configuration
    ratio_text = f"Turnover: {turnover_ratio:.1f}x"
    insight_text = f"Cada dólar depositado se apuesta ~{turnover_ratio:.1f} veces"

    chart_layout = get_base_layout()
    chart_layout.update(
        autosize=True, 
        height=280,
        barmode='group', 
        bargap=0.35,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(
            showgrid=False, 
            zeroline=False, 
            automargin=True,
            tickfont=dict(size=12, color='#475569', family='Inter')
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        legend=dict(
            orientation='h', 
            y=1.15, 
            x=0.5, 
            xanchor='center',
            font=dict(size=11, color='#64748b')
        ),
        annotations=[
            dict(
                x=0.98, 
                y=1.12, 
                xref='paper', 
                yref='paper',
                text=f"<b>{ratio_text}</b>",
                showarrow=False, 
                font=dict(size=18, color="#1E3A8A", family='Inter'),
                xanchor='right'
            ),
            dict(
                x=0.5, 
                y=-0.12, 
                xref='paper', 
                yref='paper',
                text=f"<i>{insight_text}</i>",
                showarrow=False, 
                font=dict(size=11, color='#94A3B8', family='Inter'),
                xanchor='center'
            )
        ]
    )
    figure_object.update_layout(**chart_layout)

    return figure_object
