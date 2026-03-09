import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(odds_hist):
    # 1. Data validation
    if not odds_hist or not odds_hist.get("bins"):
        return go.Figure()
        
    # 2. Data preparation
    odds_bin_values = odds_hist["bins"][:-1]
    odds_frequency_values = odds_hist["values"]

    # 3. Visual configuration
    bar_color = "#1E3A8A"  # Royal Blue
    bar_opacity = 0.95
    bar_line_config = dict(color='white', width=1.0)
    
    hover_template = (
        "Cuota: <b>%{x:,.2f}</b><br>"
        "Frecuencia: <b>%{y:,.0f}</b>"
        "<extra></extra>"
    )

    hover_label_style = dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font=dict(family="Inter", color="#1F2937")
    )

    # 4. Trace creation
    histogram_trace = go.Bar(
        x=odds_bin_values,
        y=odds_frequency_values,
        marker=dict(
            color=bar_color,
            line=bar_line_config
        ),
        opacity=bar_opacity,
        hovertemplate=hover_template
    )

    # 5. Layout configuration
    chart_layout = get_base_layout()
    chart_layout.update(
        bargap=0.1,
        xaxis=dict(
            title="", 
            showgrid=False, 
            zeroline=False
        ),
        yaxis=dict(
            title="", 
            showgrid=False, 
            zeroline=False, 
            showline=False
        ),
        margin=dict(l=40, r=20, t=30, b=40),
        hoverlabel=hover_label_style
    )

    # 6. Final figure construction
    figure_object = go.Figure(histogram_trace)
    figure_object.update_layout(**chart_layout)
    
    return figure_object
