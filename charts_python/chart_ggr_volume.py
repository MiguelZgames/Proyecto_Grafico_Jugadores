import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_daily):
    if len(df_daily) == 0:
        return go.Figure()

    x_vals = df_daily["date"].to_list()
    y_vol = df_daily["amount_usd"].to_list()
    y_ggr = df_daily["ggr_usd"].to_list()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vol,
        name='Volumen',
        mode='lines',
        line=dict(color='rgba(148, 163, 184, 0.4)', shape='spline', width=1),
        fill='tozeroy',
        fillcolor='rgba(226, 232, 240, 0.35)',
        yaxis='y2',
        hovertemplate='<b>Volumen:</b> $%{y:,.2f}<extra></extra>',
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_ggr,
        name='GGR',
        mode='lines+markers',
        line=dict(color=paleta_corpo["royalBlue"], shape='spline', width=3),
        marker=dict(size=5, color='#ffffff', line=dict(color=paleta_corpo["royalBlue"], width=2)),
        fill='tozeroy',
        fillcolor='rgba(30, 58, 138, 0.05)',
        yaxis='y1',
        hovertemplate='<b>GGR:</b> $%{y:,.2f}<extra></extra>',
        showlegend=True
    ))

    n = len(x_vals)
    if n > 1:
        sum_x = sum(range(n))
        sum_y = sum(y_ggr)
        sum_xy = sum(i * y for i, y in enumerate(y_ggr))
        sum_xx = sum(i * i for i in range(n))
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x) if (n * sum_xx - sum_x * sum_x) != 0 else 0
        b = (sum_y - m * sum_x) / n
        trend_y = [m * i + b for i in range(n)]

        mean_ggr = sum_y / n if n > 0 else 0
        rel_change = (trend_y[-1] - trend_y[0]) / abs(mean_ggr) if mean_ggr != 0 else 0
        
        trend_color = '#94a3b8'
        if abs(rel_change) > 0.05:
            trend_color = paleta_corpo["emerald"] if m > 0 else paleta_corpo["crimson"]
            
        trend_symbol = '↗' if m > 0 else ('↘' if m < 0 else '→')

        fig.add_trace(go.Scatter(
            x=x_vals, y=trend_y,
            name=f'Tendencia ({trend_symbol})',
            mode='lines',
            line=dict(color=trend_color, width=1.5, dash='dot'),
            yaxis='y1',
            hoverinfo='skip',
            showlegend=True
        ))

    layout = get_base_layout()
    layout.update(
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5, font=dict(size=11, color='#64748b')),
        margin=dict(l=65, r=65, t=30, b=40),
        xaxis=dict(
            type='category',
            rangeslider=dict(visible=True, thickness=0.04, bgcolor='#f8fafc', bordercolor='#e2e8f0', borderwidth=1),
            automargin=True,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        yaxis=dict(
            title=dict(text='Ingresos Brutos (GGR)', font=dict(size=11, color='#64748b'), standoff=15),
            tickprefix='$', tickformat='.2s',
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            gridcolor='rgba(241, 245, 249, 0.6)'
        ),
        yaxis2=dict(
            title=dict(text='Volumen Apostado', font=dict(size=11, color='#64748b'), standoff=15),
            tickprefix='$', tickformat='.2s',
            showgrid=False, zeroline=False, showline=False,
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            overlaying='y', side='right'
        ),
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.98)", bordercolor="#e2e8f0", font=dict(family="Inter", size=12, color="#1e293b")),
        dragmode='zoom', transition=dict(duration=300, easing='cubic-in-out')
    )
    fig.update_layout(**layout)
    return fig
