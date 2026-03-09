import plotly.graph_objects as go
from charts_python.utils import PRIMARY_COLOR, NEUTRAL_COLOR, NEGATIVE_COLOR, get_base_layout

def build_chart(player_risk_profile_data):
    if not player_risk_profile_data:
        return go.Figure()

    # Data preparation
    unique_systems = sorted(list(set(d["system"] for d in player_risk_profile_data)))
    
    results_order = ["Perdido", "CashOut", "Ganada"]
    semantic_colors = {
        "Ganada": "#E11D48", 
        "Perdido": "#1E3A8A", 
        "CashOut": "#64748B"
    }
    semantic_labels = {
        "Ganada": "Ganado", 
        "Perdido": "Perdido", 
        "CashOut": "CashOut"
    }

    # Derived metrics
    system_totals = {}
    for data_row in player_risk_profile_data:
        current_system = data_row["system"]
        system_totals[current_system] = system_totals.get(current_system, 0) + data_row["amount_usd"]

    # Chart traces
    figure_object = go.Figure()

    for result_type in results_order:
        filtered_data = [d for d in player_risk_profile_data if d.get("result") == result_type]
        if not filtered_data:
            continue

        category_values = []
        hover_custom_data = []
        
        for system_name in unique_systems:
            monetary_value = next((d["amount_usd"] for d in filtered_data if d["system"] == system_name), 0)
            category_values.append(monetary_value)
            
            percentage = (monetary_value / system_totals[system_name] * 100) if system_totals.get(system_name, 0) > 0 else 0
            hover_custom_data.append(f"{percentage:.0f}%")

        bar_trace = go.Bar(
            name=semantic_labels.get(result_type, result_type), 
            x=unique_systems, 
            y=category_values,
            marker=dict(color=semantic_colors.get(result_type, NEUTRAL_COLOR)),
            customdata=hover_custom_data,
            hovertemplate = (
                "Sistema: <b>%{x}</b><br>"
                "Resultado: <b>%{fullData.name}</b><br>"
                "Exposición: <b>$%{y:,.0f}</b><br>"
                "Participación: <b>%{customdata}%</b>"
                "<extra></extra>"
            )
        )
        figure_object.add_trace(bar_trace)

    # Layout configuration
    chart_layout = get_base_layout()
    chart_layout.update(
        autosize=True, 
        barmode='stack', 
        bargap=0.3,
        margin=dict(l=50, r=20, t=40, b=50),
        xaxis=dict(
            title="Sistema de Juego", 
            showgrid=False,
            tickfont=dict(size=11, color='#475569', family='Inter')
        ),
        yaxis=dict(
            title="Exposición (USD)", 
            tickprefix='$', 
            tickformat=',.0f',
            gridcolor='rgba(0,0,0,0.05)', 
            zeroline=False,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        legend=dict(
            orientation='h', 
            y=1.08, 
            x=0.5, 
            xanchor='center',
            font=dict(size=11, color='#64748b')
        )
    )
    figure_object.update_layout(**chart_layout)

    return figure_object
