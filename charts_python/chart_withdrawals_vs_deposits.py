import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_daily):
    if len(df_daily) == 0:
        return go.Figure()

    x_vals = df_daily["date"].to_list()
    y_dep = df_daily["deposits"].to_list()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_dep, name='Depósitos', mode='lines',
        line=dict(color=paleta_corpo["emerald"], width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(16,185,129,0.12)',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Depósitos: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    n = len(x_vals)
    if n > 1:
        s_x, s_y = sum(range(n)), sum(y_dep)
        s_xy, s_xx = sum(i * y for i, y in enumerate(y_dep)), sum(i * i for i in range(n))
        d = n * s_xx - s_x * s_x
        m = (n * s_xy - s_x * s_y) / d if d else 0
        b = (s_y - m * s_x) / n
        fig.add_trace(go.Scatter(
            x=x_vals, y=[m * i + b for i in range(n)], name='Tendencia', mode='lines',
            line=dict(color=paleta_corpo["crimson"], width=2, dash='dot'),
            hoverinfo='skip'
        ))

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_dep, name='Retiros', mode='lines+markers',
        line=dict(color=paleta_corpo["royalBlue"], width=2, shape='spline'),
        marker=dict(size=4, color='#ffffff', line=dict(color=paleta_corpo["royalBlue"], width=1.5)),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Retiros: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    layout = get_base_layout()
    layout.update(
        hovermode='x unified',
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', font=dict(size=11, color='#64748b')),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(title="Fecha", tickformat="%b %Y", dtick="M1", tickangle=-30, showgrid=False,
                   automargin=True, tickfont=dict(size=11, color='#64748b', family='Inter')),
        yaxis=dict(title="USD", tickprefix='$', tickformat=',.0f', gridcolor='rgba(0,0,0,0.05)',
                   zeroline=False, tickfont=dict(size=11, color='#64748b', family='Inter')),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", size=12, color="#1F2937")),
        dragmode='zoom'
    )
    fig.update_layout(**layout)
    return fig
