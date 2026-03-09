import plotly.graph_objects as go
from charts_python.utils import PRIMARY_COLOR, NEUTRAL_COLOR, NEGATIVE_COLOR, get_base_layout

def build_chart(player_ticket_statistics):
    if not player_ticket_statistics:
        return go.Figure()

    # Data preparation & Category normalization
    valid_categories = {"Perdido", "Ganada", "CashOut"}
    category_counts = {"Perdido": 0, "Ganada": 0, "CashOut": 0, "Otros": 0}
    category_ggr = {"Perdido": 0.0, "Ganada": 0.0, "CashOut": 0.0, "Otros": 0.0}

    for d in player_ticket_statistics:
        status = d.get("status_bet", "Otros")
        count = d.get("_count", 0)
        ggr = d.get("ggr_usd", 0.0)
        
        if status in valid_categories:
            category_counts[status] += count
            category_ggr[status] += ggr
        else:
            category_counts["Otros"] += count
            category_ggr["Otros"] += ggr

    ticket_status_labels = []
    ticket_counts = []
    ggr_values_by_status = []
    
    # Ensure they are added in a specific order if preferred, or just dynamically
    for status in ["Perdido", "Ganada", "CashOut", "Otros"]:
        if category_counts[status] > 0:
            ticket_status_labels.append(status)
            ticket_counts.append(category_counts[status])
            ggr_values_by_status.append(category_ggr[status])

    # Color mapping
    pos_colors = [
        "#1E3A8A", "#334155", "#3F546A", "#4C5F75", "#586A80",
        "#64748B", "#6D8299", "#7A8DA3", "#94A3B8", "#A7B1C2",
        "#B8C4D4", "#CBD5E1", "#E2E8F0"
    ]
    neg_colors = ["#BE123C", "#E11D48"]

    ticket_color_mapping = {
        "Perdido": pos_colors[0],  # #1E3A8A
        "CashOut": pos_colors[5],  # #64748B
        "Ganada": neg_colors[1],   # #E11D48
        "Otros": pos_colors[10]    # #B8C4D4
    }

    slice_colors = [ticket_color_mapping[status] for status in ticket_status_labels]

    # Metric calculations
    total_tickets = sum(ticket_counts)
    pull_factors = [0.04 if count == max(ticket_counts) else 0 for count in ticket_counts]

    hover_custom_data = [[float(ggr)] for ggr in ggr_values_by_status]

    text_information = [
        f"{ticket_status_labels[i]}<br>{(count / total_tickets):.1%}" if (total_tickets > 0 and (count / total_tickets) > 0.02) else "" 
        for i, count in enumerate(ticket_counts)
    ]

    # Pie chart trace
    figure_object = go.Figure(go.Pie(
        labels=ticket_status_labels, 
        values=ticket_counts, 
        hole=0.5,
        marker=dict(colors=slice_colors, line=dict(color="white", width=2)),
        textinfo="text", 
        text=text_information,
        textfont=dict(size=12, color="white", family="Inter"),
        customdata=hover_custom_data,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "──────────<br>"
            "Tickets: <b>%{value:,}</b><br>"
            "GGR: <b>$%{customdata[0]:,.0f}</b>"
            "<extra></extra>"
        ),
        pull=pull_factors
    ))

    # Layout configuration
    chart_layout = get_base_layout()
    chart_layout.update(
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, family="Inter")
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#1F2937")
        ),
        annotations=[
            dict(
                font=dict(size=11, color=NEUTRAL_COLOR, family="Inter"),
                showarrow=False, 
                text="Total Tickets", 
                x=0.5, 
                y=0.55
            ),
            dict(
                font=dict(size=18, color=PRIMARY_COLOR, family="Inter", weight="bold" if hasattr(dict, "__class__") else None),
                showarrow=False, 
                text=f"<b>{total_tickets:,}</b>", 
                x=0.5, 
                y=0.45
            )
        ]
    )
    figure_object.update_layout(**chart_layout)

    return figure_object
