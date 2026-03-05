import plotly.graph_objects as go
import polars as pl
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()

    # 1. Ordenar por deposits descendente y 2. Calcular ROI
    df = df_segments.sort("deposits", descending=True).with_columns(
        (pl.col("ggr_usd") / pl.col("deposits")).alias("roi")
    )

    x_vals = df["group_name"].to_list()
    y_ggr = df["ggr_usd"].to_list()
    y_dep = df["deposits"].to_list()
    roi_vals = df["roi"].to_list()

    # Datos para tooltip: [GGR, Depósitos, ROI]
    custom_data = list(zip(y_ggr, y_dep, roi_vals))
    
    # Tooltip con formato profesional
    hovertemplate = (
        "<b>Segmento:</b> %{x}<br>" +
        "<b>GGR:</b> $%{customdata[0]:,.0f}<br>" +
        "<b>Depósitos:</b> $%{customdata[1]:,.0f}<br>" +
        "<b>ROI:</b> %{customdata[2]:.1%}<extra></extra>"
    )

    fig = go.Figure()

    # Traza GGR
    fig.add_trace(go.Bar(
        x=x_vals, y=y_ggr, name='GGR',
        marker=dict(color=paleta_corpo["emerald"]),
        customdata=custom_data, hovertemplate=hovertemplate
    ))

    # Traza Depósitos
    fig.add_trace(go.Bar(
        x=x_vals, y=y_dep, name='Depósitos',
        marker=dict(color=paleta_corpo["teal"]),
        customdata=custom_data, hovertemplate=hovertemplate
    ))

    layout = get_base_layout()
    layout.update(
        barmode='group', 
        bargap=0.22, 
        bargroupgap=0.06,
        xaxis_tickangle=-35,
        margin=dict(l=40, r=20, t=40, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(family="Inter", color="#2D3748")
        )
    )
    fig.update_layout(**layout)
    return fig
