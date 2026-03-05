import numpy as np
import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(df_segments):

    if len(df_segments) == 0:
        return go.Figure()

    x = df_segments["deposits"]
    y = df_segments["ggr_usd"]
    segments = df_segments["group_name"]

    slope, intercept = np.polyfit(x, y, 1)
    x_trend = np.linspace(min(x), max(x), 100)
    y_trend = slope * x_trend + intercept

    if slope > 0:
        trend_text = "Eficiencia positiva"
    elif slope < 0:
        trend_text = "Eficiencia negativa"
    else:
        trend_text = "Eficiencia estable"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(
            size=22,
            color=y,
            colorscale="RdYlGn",
            opacity=0.9
        ),
        text=segments,
        hovertemplate=
        "<b>%{text}</b><br>" +
        "Depósitos: <b>$%{x:,.0f}</b><br>" +
        "GGR: <b>$%{y:,.0f}</b><extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=x_trend,
        y=y_trend,
        mode="lines",
        line=dict(
            color="#2563EB",
            dash="dot",
            width=3
        ),
        name="Tendencia"
    ))

    layout = get_base_layout()

    layout.update(

        height=420,

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
            )
        ],

        annotations=[
            dict(
                x=min(x),
                y=max(y),
                text=f"<b>{trend_text}</b>",
                showarrow=False,
                font=dict(size=13)
            )
        ]
    )

    fig.update_layout(**layout)

    return fig
