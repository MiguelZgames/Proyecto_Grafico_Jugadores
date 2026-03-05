import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_daily):
    if len(df_daily) == 0:
        return go.Figure()

    x_vals = df_daily["date"].to_list()
    y_vol = df_daily["amount_usd"].to_list()
    y_ggr = df_daily["ggr_usd"].to_list()

    fig = go.Figure()

    # Volumen: área gris de fondo (contextual)
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vol,
        name='Volumen Apostado',
        mode='lines',
        line=dict(color='rgba(148,163,184,0.6)', width=2, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(148,163,184,0.12)',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Volumen: <b>$%{y:,.0f}</b><extra></extra>",
        showlegend=True
    ))

    # GGR: serie principal (sin fill)
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_ggr,
        name='GGR',
        mode='lines+markers',
        line=dict(color=paleta_corpo["royalBlue"], width=2.8, shape='spline'),
        marker=dict(size=5, color='#ffffff', line=dict(color=paleta_corpo["royalBlue"], width=2)),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>GGR: <b>$%{y:,.0f}</b><extra></extra>",
        showlegend=True
    ))

    # Tendencia GGR
    n = len(x_vals)
    if n > 1:
        sum_x = sum(range(n))
        sum_y = sum(y_ggr)
        sum_xy = sum(i * y for i, y in enumerate(y_ggr))
        sum_xx = sum(i * i for i in range(n))
        denom = n * sum_xx - sum_x * sum_x
        m = (n * sum_xy - sum_x * sum_y) / denom if denom != 0 else 0
        b = (sum_y - m * sum_x) / n
        trend_y = [m * i + b for i in range(n)]

        mean_ggr = sum_y / n if n > 0 else 0
        rel_change = (trend_y[-1] - trend_y[0]) / abs(mean_ggr) if mean_ggr != 0 else 0

        trend_color = '#94a3b8'
        if abs(rel_change) > 0.05:
            trend_color = paleta_corpo["emerald"] if m > 0 else paleta_corpo["crimson"]

        fig.add_trace(go.Scatter(
            x=x_vals, y=trend_y,
            name='Tendencia',
            mode='lines',
            line=dict(color=trend_color, width=1.5, dash='dot'),
            hoverinfo='skip',
            showlegend=True
        ))

    layout = get_base_layout()
    layout.update(
        hovermode='x unified',
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', font=dict(size=11, color='#64748b')),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            tickformat="%b %Y",
            dtick="M1",
            tickangle=-30,
            showgrid=False,
            automargin=True,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        yaxis=dict(
            tickprefix='$',
            tickformat=',.0f',
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False
        ),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", size=12, color="#1F2937")),
        dragmode='zoom'
    )
    fig.update_layout(**layout)
    return fig
