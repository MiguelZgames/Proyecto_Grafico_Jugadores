import numpy as np
import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(dataframe_segments):

    if len(dataframe_segments) == 0:
        return go.Figure()

    # Data preparation
    segment_deposit_values = dataframe_segments["deposits"].to_list()
    segment_ggr_values = dataframe_segments["ggr_usd"].to_list()
    segment_labels = dataframe_segments["group_name"].to_list()

    if len(segment_deposit_values) == 0:
        return go.Figure()

    deposits_array = np.array(segment_deposit_values)
    ggr_array = np.array(segment_ggr_values)

    # Derived metrics
    segment_roi_values = [
        (g / d) if d > 0 else 0 
        for g, d in zip(segment_ggr_values, segment_deposit_values)
    ]
    hover_custom_data = list(zip(segment_ggr_values, segment_deposit_values, segment_roi_values))

    if len(deposits_array) > 1:
        trend_slope, trend_intercept = np.polyfit(deposits_array, ggr_array, 1)
    else:
        trend_slope, trend_intercept = 0, 0
        
    trend_x_values = np.linspace(min(deposits_array), max(deposits_array), 100)
    trend_y_values = trend_slope * trend_x_values + trend_intercept

    if trend_slope > 0:
        trend_text = "Tendencia positiva: más depósitos generan mayor GGR"
    elif trend_slope < 0:
        trend_text = "Tendencia negative: más depósitos no generan mayor GGR"
    else:
        trend_text = "Tendencia estable: sin correlación clara"

    highlight_index = int(np.argmax(ggr_array))
    point_sizes = [16] * len(segment_deposit_values)
    point_sizes[highlight_index] = 26
    
    color_royal_blue = "#1E3A8A"
    color_slate_blue = "#94A3B8"
    color_crimson = "#E11D48"

    point_colors = [color_royal_blue if g >= 0 else color_crimson for g in segment_ggr_values]

    # Chart traces
    figure_object = go.Figure()

    hover_template = (
        "<b>Segmento:</b> %{text}<br>"
        "<b>GGR:</b> $%{customdata[0]:,.0f}<br>"
        "<b>Depósitos:</b> $%{customdata[1]:,.0f}<br>"
        "<b>ROI:</b> %{customdata[2]:.1%}<extra></extra>"
    )

    scatter_trace = go.Scatter(x=segment_deposit_values, y=segment_ggr_values, mode="markers",
        marker=dict(size=point_sizes, color=point_colors, opacity=0.85, line=dict(color="white", width=1.5)),
        text=segment_labels, customdata=hover_custom_data, hovertemplate=hover_template, name="Segmentos")
    figure_object.add_trace(scatter_trace)

    trend_trace = go.Scatter(x=trend_x_values, y=trend_y_values, mode="lines",
        line=dict(color=color_slate_blue, dash="dash", width=3), name="Tendencia")
    figure_object.add_trace(trend_trace)

    # Layout configuration
    average_deposits = float(np.mean(deposits_array))
    
    chart_layout = get_base_layout()
    chart_layout.update(height=420, margin=dict(t=30, b=40, l=60, r=20),
        xaxis=dict(title="Depósitos (USD)", showgrid=False, showspikes=False),
        yaxis=dict(title="GGR (USD)", showgrid=False, showspikes=False),
        shapes=[
            dict(type="line", x0=min(segment_deposit_values), x1=max(segment_deposit_values), y0=0, y1=0,
                line=dict(color=color_slate_blue, dash="dash")
            ),
            dict(type="line", x0=average_deposits, x1=average_deposits, y0=min(segment_ggr_values), y1=max(segment_ggr_values),
                line=dict(color="#CBD5E1", dash="dot")
            )
        ],
        annotations=[dict(x=0.02, y=0.98, xref="paper", yref="paper", text=trend_text, showarrow=False,
            font=dict(size=12, color="#475569"), align="left")],
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(color="#1F2937", family="Inter", size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    figure_object.update_layout(**chart_layout)

    return figure_object
