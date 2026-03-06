import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_daily):
    if not p_daily:
        return go.Figure()

    x_vals = [d["date"] for d in p_daily]
    y_prof = [d["profit_usd"] for d in p_daily]
    y_dep = [d["deposits"] for d in p_daily]

    fig = go.Figure()

    # Depósitos: serie principal con área sombreada
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_dep, name='Depósitos', mode='lines',
        line=dict(color=paleta_corpo["emerald"], width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(16,185,129,0.12)',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Depósitos: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    # Profit: serie secundaria
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_prof, name='Profit', mode='lines+markers',
        line=dict(color=paleta_corpo["royalBlue"], width=2, shape='spline'),
        marker=dict(size=4, color='#ffffff', line=dict(color=paleta_corpo["royalBlue"], width=1.5)),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Profit: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    # Tendencia: regresión lineal sobre Profit
    n = len(x_vals)
    if n > 1:
        s_x, s_y = sum(range(n)), sum(y_prof)
        s_xy = sum(i * y for i, y in enumerate(y_prof))
        s_xx = sum(i * i for i in range(n))
        d = n * s_xx - s_x * s_x
        m = (n * s_xy - s_x * s_y) / d if d else 0
        b = (s_y - m * s_x) / n
        fig.add_trace(go.Scatter(
            x=x_vals, y=[m * i + b for i in range(n)],
            name='Tendencia', mode='lines',
            line=dict(color=paleta_corpo["crimson"], width=2, dash='dot'),
            hoverinfo='skip'
        ))

    layout = get_base_layout()
    layout.update(
        autosize=True, height=420,
        hovermode='x unified',
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', font=dict(size=11, color='#64748b')),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(tickformat="%b %d", showgrid=False, automargin=True,
                   tickfont=dict(size=11, color='#64748b', family='Inter')),
        yaxis=dict(tickprefix='$', tickformat=',.0f', gridcolor='rgba(0,0,0,0.05)',
                   zeroline=False, autorange=True,
                   tickfont=dict(size=11, color='#64748b', family='Inter')),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", size=12, color="#1F2937")),
        dragmode='zoom'
    )
    fig.update_layout(**layout)
    return fig
