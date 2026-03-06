import numpy as np
import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(df_segments):

    if len(df_segments) == 0:
        return go.Figure()

    x = df_segments["deposits"].to_list()
    y = df_segments["ggr_usd"].to_list()
    segments = df_segments["group_name"].to_list()

    if len(x) == 0:
        return go.Figure()

    x_np = np.array(x)
    y_np = np.array(y)

    if len(x_np) > 1:
        slope, intercept = np.polyfit(x_np, y_np, 1)
    else:
        slope, intercept = 0, 0
    x_trend = np.linspace(min(x_np), max(x_np), 100)
    y_trend = slope * x_trend + intercept

    if slope > 0:
        trend_text = "Tendencia positiva: más depósitos generan mayor GGR"
    elif slope < 0:
        trend_text = "Tendencia negativa: más depósitos no generan mayor GGR"
    else:
        trend_text = "Tendencia estable: sin correlación clara"

    # Mejora 2 — Destacar segmento con mayor GGR
    highlight_idx = int(np.argmax(y_np))
    sizes = [18] * len(x)
    sizes[highlight_idx] = 28

    fig = go.Figure()

    # Mejora 1 — Scatter con jerarquía visual y opacidad reducida
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(
            size=sizes,
            color=y,
            coloraxis="coloraxis",
            opacity=0.65,
            line=dict(color="white", width=2)
        ),
        text=segments,
        # Mejora 5 — Tooltip mejorado
        hovertemplate=
        "<b>Segmento:</b> %{text}<br>" +
        "<b>Depósitos:</b> $%{x:,.0f}<br>" +
        "<b>GGR:</b> $%{y:,.0f}<br>" +
        "<i>Conversión de depósitos en ingresos</i><extra></extra>"
    ))

    # Mejora 3 — Tendencia más visible
    fig.add_trace(go.Scatter(
        x=x_trend,
        y=y_trend,
        mode="lines",
        line=dict(
            color="#1D4ED8",
            dash="dash",
            width=4
        ),
        name="Tendencia"
    ))

    layout = get_base_layout()

    # Mejora 4 — Cuadrante analítico (línea vertical en promedio depósitos)
    avg_x = float(np.mean(x_np))

    layout.update(

        height=420,

        coloraxis=dict(
            colorscale="RdYlGn",
            cmin=min(y),
            cmax=max(y),
            cmid=0,
            showscale=False
        ),

        xaxis=dict(
            title="Depósitos (USD)",
            showgrid=False
        ),

        yaxis=dict(
            title="GGR (USD)",
            showgrid=False
        ),

        shapes=[
            dict(
                type="line",
                x0=min(x),
                x1=max(x),
                y0=0,
                y1=0,
                line=dict(
                    color="#94A3B8",
                    dash="dash"
                )
            ),
            dict(
                type="line",
                x0=avg_x,
                x1=avg_x,
                y0=min(y),
                y1=max(y),
                line=dict(
                    color="#CBD5E1",
                    dash="dot"
                )
            )
        ],

        annotations=[
            dict(
                x=0.02,
                y=0.95,
                xref="paper",
                yref="paper",
                text=trend_text,
                showarrow=False,
                font=dict(size=12, color="#475569"),
                align="left"
            )
        ],

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(color="#1F2937", family="Inter", size=12)
        )
    )

    fig.update_layout(**layout)

    return fig
