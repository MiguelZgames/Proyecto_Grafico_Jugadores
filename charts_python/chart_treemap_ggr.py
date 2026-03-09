import plotly.graph_objects as go

def build_chart(df_segments):

    # Return empty figure if dataset is empty
    if len(df_segments) == 0:
        return go.Figure()

    # Data preparation
    filtered_segments = (
        df_segments
        .filter(df_segments["ggr_usd"] != 0)
        .sort("ggr_usd", descending=True)
    )

    if len(filtered_segments) == 0:
        return go.Figure()

    segment_labels = filtered_segments["group_name"].to_list()      # Etiquetas
    actual_values = filtered_segments["ggr_usd"].to_list()          # Valores reales
    segment_sizes = [abs(v) for v in actual_values]                 # Tamaños absolutos para Plotly
    
    total_ggr = sum(actual_values)                                  # GGR total
    total_size = sum(segment_sizes)                                 # Tamaño total para treemap

    # Color palettes
    pos_colors = [
        "#1E3A8A", "#334155", "#3F546A", "#4C5F75", "#586A80",
        "#64748B", "#6D8299", "#7A8DA3", "#94A3B8", "#A7B1C2",
        "#B8C4D4", "#CBD5E1", "#E2E8F0"
    ]
    neg_colors = ["#BE123C", "#E11D48"]

    assigned_colors = ["white"]
    p_idx, n_idx = 0, 0
    for val in actual_values:
        if val > 0:
            assigned_colors.append(pos_colors[p_idx % len(pos_colors)])
            p_idx += 1
        else:
            assigned_colors.append(neg_colors[n_idx % len(neg_colors)])
            n_idx += 1

    # Monetary formatter
    def format_currency(value):
        sign = "-" if value < 0 else ""
        abs_val = abs(value)
        if abs_val >= 1_000_000:
            return f"{sign}${abs_val / 1_000_000:.1f}M"
        elif abs_val >= 1_000:
            return f"{sign}${abs_val / 1_000:.1f}K"
        return f"{sign}${abs_val:,.0f}"

    # Treemap text labels
    treemap_text = [
        f"{segment}<br>{format_currency(value)}<br>{(value / total_ggr) * 100:.1f}%" if total_ggr else f"{segment}<br>{format_currency(value)}<br>0.0%"
        for segment, value in zip(segment_labels, actual_values)
    ]

    # Treemap figure
    fig = go.Figure(
        go.Treemap(

            branchvalues="total",

            labels=["Global"] + segment_labels,
            parents=[""] + ["Global"] * len(segment_labels),
            values=[total_size] + segment_sizes,

            text=["Global"] + treemap_text,
            texttemplate="<b>%{text}</b>",

            textfont=dict(color="white", size=14, family="Inter"),

            marker=dict(
                colors=assigned_colors,
                line=dict(width=1.5, color="white")
            ),

            customdata=[total_ggr] + actual_values,
            hovertemplate="<b>%{label}</b>"
            "<br>GGR: <b>%{customdata:$,.0f}</b>"
            "<br>Share: <b>%{percentParent:.1%}</b>"
            "<extra></extra>"
        )
    )

    # Layout configuration
    fig.update_layout(height=520,
        margin=dict(t=0, l=0, r=0, b=0),
        uniformtext=dict(mode="hide", minsize=11),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", align="left", namelength=-1)
    )

    return fig