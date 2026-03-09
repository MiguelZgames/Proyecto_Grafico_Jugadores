import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout


def build_chart(df_daily):
    if len(df_daily) == 0:
        return go.Figure()

    # ── Data preparation ──
    date_values = df_daily["date"].to_list()            # Fechas
    volume_values = df_daily["amount_usd"].to_list()    # Monto apostado
    ggr_values = df_daily["ggr_usd"].to_list()          # GGR

    # ── Figure initialization ──
    fig = go.Figure()

    # ── Volume trace: contextual series with shaded area ──
    fig.add_trace(go.Scatter(
        x=date_values, y=volume_values,
        name='Monto Apostado', mode='lines',
        line=dict(color='rgba(148,163,184,0.6)', width=2, shape='spline'),
        fill='tozeroy', fillcolor='rgba(148,163,184,0.12)',
        hovertemplate="Monto Apostado: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    # ── Trend calculation: linear regression on GGR ──
    n_points = len(date_values)

    if n_points > 1:
        sum_x = sum(range(n_points))
        sum_y = sum(ggr_values)
        sum_xy = sum(i * y for i, y in enumerate(ggr_values))
        sum_xx = sum(i * i for i in range(n_points))

        denominator = n_points * sum_xx - sum_x * sum_x
        slope = (n_points * sum_xy - sum_x * sum_y) / denominator if denominator else 0
        intercept = (sum_y - slope * sum_x) / n_points

        trend_values = [slope * i + intercept for i in range(n_points)]

        # ── Trend trace ──
        fig.add_trace(go.Scatter(
            x=date_values, y=trend_values,
            name='Tendencia', mode='lines',
            line=dict(color=paleta_corpo["crimson"], width=2, dash='dot'),
            hoverinfo='skip'
        ))

    # ── GGR trace: primary series ──
    fig.add_trace(go.Scatter(
        x=date_values, y=ggr_values,
        name='GGR', mode='lines+markers',
        line=dict(color=paleta_corpo["royalBlue"], width=2, shape='spline'),
        marker=dict(size=4, color='#ffffff',
                    line=dict(color=paleta_corpo["royalBlue"], width=1.5)),
                    showlegend=True,
        hovertemplate="GGR: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    # ── Layout configuration ──
    layout = get_base_layout()

    layout.update(
        hovermode='x unified',
        legend=dict(
            orientation='h', y=1.10, x=0.5, xanchor='center',
            font=dict(size=11, color='#64748b'),
            traceorder="normal", entrywidth=100, entrywidthmode='pixels'
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            tickformat="%b %Y", dtick="M1", tickangle=-30,
            showgrid=False, automargin=True,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        yaxis=dict(
            tickprefix='$', tickformat=',.0f',
            gridcolor='rgba(0,0,0,0.05)', zeroline=False,
            tickfont=dict(size=11, color='#64748b', family='Inter')
        ),
        hoverlabel=dict(
            bgcolor="white", bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        dragmode='zoom'
    )

    fig.update_layout(**layout)

    # ── Return figure ──
    return fig
