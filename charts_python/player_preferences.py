import plotly.graph_objects as go
from charts_python.utils import PRIMARY_COLOR, NEUTRAL_COLOR, NEGATIVE_COLOR, get_base_layout

def build_chart(player_preferences_data):
    if not player_preferences_data:
        return go.Figure()

    # Data preparation
    bet_types = [d["type_bet"] for d in player_preferences_data]
    bet_amounts = [d["amount_usd"] for d in player_preferences_data]
    bet_counts = [d.get("_count", 0) for d in player_preferences_data]

    # Color palettes
    pos_colors = [
        "#1E3A8A", "#334155", "#3F546A", "#4C5F75", "#586A80",
        "#64748B", "#6D8299", "#7A8DA3", "#94A3B8", "#A7B1C2",
        "#B8C4D4", "#CBD5E1", "#E2E8F0"
    ]

    neg_colors = ["#BE123C", "#E11D48"]

    pie_colors = [pos_colors[i % len(pos_colors)] for i in range(len(bet_types))]

    # Derived metrics
    total_bet_amount = sum(bet_amounts)
    total_bet_count = sum(bet_counts)

    # Only show label for dominant segments
    bet_percentages = [(amount / total_bet_amount * 100) if total_bet_amount > 0 else 0 for amount in bet_amounts]
    text_information = [f"{bet_types[i]}<br>{bet_percentages[i]:.1f}%" if bet_percentages[i] > 15 else "" for i in range(len(bet_types))]

    pull_factors = [0.03 if pct == max(bet_percentages) else 0 for pct in bet_percentages]

    # Chart traces
    figure_object = go.Figure(go.Pie(
        labels=bet_types, 
        values=bet_amounts, 
        hole=0.55,
        marker=dict(colors=pie_colors, line=dict(color='white', width=2)),
        textinfo='text', 
        text=bet_counts,
        textfont=dict(size=12, color='white', family='Inter'),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "──────────<br>"
            "Monto apostado: <b>$%{value:,.0f}</b><br>"
            "Participación: <b>%{percent:.1%}</b><br>"
            "Apuestas realizadas: <b>%{text}</b>"
            "<extra></extra>"
        ),
        pull=pull_factors
    ))

    # Layout configuration
    chart_layout = get_base_layout()
    chart_layout.update(
        autosize=True,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(
            orientation='h', 
            y=-0.05, 
            x=0.5, 
            xanchor='center',
            font=dict(size=11, color='#64748b', family='Inter')
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        annotations=[
            dict(
                font=dict(size=11, color=NEUTRAL_COLOR, family='Inter'),
                showarrow=False, 
                text="Total Apostado", 
                x=0.5, 
                y=0.55
            ),
            dict(
                font=dict(size=18, color=PRIMARY_COLOR, family='Inter', weight='bold' if hasattr(dict, '__class__') else None),
                showarrow=False, 
                text=f"<b>${total_bet_amount:,.0f}</b>", 
                x=0.5, 
                y=0.45
            )
        ]
    )
    figure_object.update_layout(**chart_layout)

    return figure_object
