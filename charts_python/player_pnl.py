import plotly.graph_objects as go
from charts_python.utils import PRIMARY_COLOR, NEUTRAL_COLOR, NEGATIVE_COLOR, get_base_layout

def build_chart(player_daily_data):
    if not player_daily_data:
        return go.Figure()

    # Data preparation
    date_values = [d["date"] for d in player_daily_data]
    profit_values = [d["profit_usd"] for d in player_daily_data]
    deposit_values = [d["deposits"] for d in player_daily_data]

    # Derived metrics
    number_of_points = len(date_values)
    trend_y_values = []
    
    if number_of_points > 1:
        sum_x = sum(range(number_of_points))
        sum_y = sum(profit_values)
        sum_xy = sum(i * y for i, y in enumerate(profit_values))
        sum_xx = sum(i * i for i in range(number_of_points))
        
        denominator = number_of_points * sum_xx - sum_x * sum_x
        trend_slope = (number_of_points * sum_xy - sum_x * sum_y) / denominator if denominator else 0
        trend_intercept = (sum_y - trend_slope * sum_x) / number_of_points
        trend_y_values = [trend_slope * i + trend_intercept for i in range(number_of_points)]

    point_colors = [PRIMARY_COLOR if p >= 0 else NEGATIVE_COLOR for p in profit_values]

    # Chart traces
    figure_object = go.Figure()

    # Depósitos (Volumen neutral) -> Slate Blue
    deposits_trace = go.Scatter(
        x=date_values, 
        y=deposit_values, 
        name='Depósitos', 
        mode='lines',
        line=dict(color=NEUTRAL_COLOR, width=3, shape='spline'),
        fill='tozeroy', 
        fillcolor='rgba(148, 163, 184, 0.12)', # Slate Blue con opacidad
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Depósitos: <b>$%{y:,.0f}</b><extra></extra>"
    )
    figure_object.add_trace(deposits_trace)

    # Profit (Métrica Principal y Negativos) -> Royal Blue / Crimson en marcadores
    profit_trace = go.Scatter(
        x=date_values, 
        y=profit_values, 
        name='Profit', 
        mode='lines+markers',
        line=dict(color=PRIMARY_COLOR, width=2, shape='spline'),
        marker=dict(
            size=5, 
            color=point_colors, 
            line=dict(color='white', width=1)
        ),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Profit: <b>$%{y:,.0f}</b><extra></extra>"
    )
    figure_object.add_trace(profit_trace)

    if number_of_points > 1:
        trend_trace = go.Scatter(
            x=date_values, 
            y=trend_y_values,
            name='Tendencia', 
            mode='lines',
            line=dict(color= NEGATIVE_COLOR, width=2, dash='dot'),
            hoverinfo='skip'
        )
        figure_object.add_trace(trend_trace)

    # Layout configuration
    chart_layout = get_base_layout()
    chart_layout.update(
        autosize=True, 
        height=420,
        hovermode='x unified',
        legend=dict(
            orientation='h', 
            y=1.08, 
            x=0.5, 
            xanchor='center', 
            font=dict(size=11, color='#64748b')
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            tickformat="%b %d", 
            showgrid=False, 
            automargin=True,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        yaxis=dict(
            tickprefix='$', 
            tickformat=',.0f', 
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False, 
            autorange=True,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0", 
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        dragmode='zoom'
    )
    figure_object.update_layout(**chart_layout)

    return figure_object
