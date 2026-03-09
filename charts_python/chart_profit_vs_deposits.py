import plotly.graph_objects as go
import polars as pl
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()

    # Data preparation
    df = df_segments.sort("deposits", descending=True).with_columns(
        (pl.col("ggr_usd") / pl.col("deposits")).alias("roi")
    )

    segment_names = df["group_name"].to_list()
    ggr_values = df["ggr_usd"].to_list()
    deposit_values = df["deposits"].to_list()
    roi_values = df["roi"].to_list()

    custom_data = list(zip(ggr_values, deposit_values, roi_values))

    # Visual configurations
    color_royal_blue = "#1E3A8A"
    color_slate_blue = "#94A3B8"
    color_crimson = "#E11D48"

    ggr_bar_colors = [color_royal_blue if v >= 0 else color_crimson for v in ggr_values]
    deposit_bar_color = color_slate_blue

    bar_border_style = dict(width=0.6, color="rgba(0,0,0,0.15)")
    
    hover_label_style = dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font=dict(family="Inter", color="#2D3748")
    )

    hover_template = (
        "<b>Segmento:</b> %{x}<br>" +
        "<b>GGR:</b> $%{customdata[0]:,.0f}<br>" +
        "<b>Depósitos:</b> $%{customdata[1]:,.0f}<br>" +
        "<b>ROI:</b> %{customdata[2]:.1%}<extra></extra>"
    )

    # Figure initialization
    fig = go.Figure()

    # GGR Trace
    fig.add_trace(go.Bar(
        x=segment_names, y=ggr_values, name='GGR',
        marker=dict(color=ggr_bar_colors, line=bar_border_style),
        customdata=custom_data, hovertemplate=hover_template
    ))

    # Deposits Trace
    fig.add_trace(go.Bar(
        x=segment_names, y=deposit_values, name='Depósitos',
        marker=dict(color=deposit_bar_color, line=bar_border_style),
        customdata=custom_data, hovertemplate=hover_template
    ))

    # Layout configuration
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
        hoverlabel=hover_label_style
    )
    
    fig.update_layout(**layout)
    
    return fig
