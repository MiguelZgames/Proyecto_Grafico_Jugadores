import plotly.graph_objects as go
import polars as pl
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_house_risk):
    # 1. Validación de datos
    if not df_house_risk or len(df_house_risk) == 0:
        return go.Figure()

    # 2. Preparación de datos
    house_risk_dataframe = pl.DataFrame(df_house_risk)

    # 3. Cálculo de métricas
    # El cálculo de "House Profit = Amount Lost - Amount Won" se realiza 
    # previamente en Polars en el script principal; aquí extraemos esos resultados.
    bet_type_values = house_risk_dataframe["type_bet"].to_list()
    house_profit_values = house_risk_dataframe["profit"].to_list()

    # 4. Preparación de colores
    color_royal_blue = "#1E3A8A"
    color_slate_blue = "#94A3B8"
    color_crimson = "#E11D48"

    bar_colors = []
    for profit in house_profit_values:
        if profit > 0:
            bar_colors.append(color_royal_blue)
        elif profit < 0:
            bar_colors.append(color_crimson)
        else:
            bar_colors.append(color_slate_blue)

    # 5. Construcción del gráfico
    hover_template = (
        "Tipo de apuesta: <b>%{x}</b><br>"
        "Profit Casa: <b>$%{y:,.2f}</b><extra></extra>"
    )

    fig = go.Figure(go.Bar(
        x=bet_type_values,
        y=house_profit_values,
        marker=dict(color=bar_colors, opacity=1.0, line=dict(width=0.6, color='rgba(0,0,0,0.15)')),
        hovertemplate=hover_template
    ))

    # 6. Configuración del layout
    base_layout = get_base_layout()
    base_layout.update(
        yaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#94A3B8", tickformat=",.0f"),
        xaxis=dict(title="", showgrid=False),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", color="#1F2937")),
        margin=dict(l=40, r=20, t=40, b=60)
    )
    
    fig.update_layout(**base_layout)

    # 7. Retorno de la figura
    return fig
