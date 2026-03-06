import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

# Semantic color mapping
_COLORS = {
    "Perdido": paleta_corpo["crimson"],
    "Ganada": paleta_corpo["emerald"],
    "CashOut": "#38BDF8",
}
_DEFAULT = "#E5E7EB"

def build_chart(p_ticket):
    if not p_ticket:
        return go.Figure()

    labels = [d["status_bet"] for d in p_ticket]
    values = [d["_count"] for d in p_ticket]
    colors = [_COLORS.get(l, _DEFAULT) for l in labels]

    total = sum(values)
    pcts = [(v / total * 100) if total > 0 else 0 for v in values]

    # Only show text for slices > 2%
    text_info = [f"{labels[i]}<br>{pcts[i]:.1f}%" if pcts[i] > 2 else "" for i in range(len(labels))]

    custom = [[float(pcts[i]), int(values[i])] for i in range(len(labels))]

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='text', text=text_info,
        textfont=dict(size=12, color='white', family='Inter'),
        customdata=custom,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "──────────<br>"
            "Tickets: <b>%{value:,}</b><br>"
            "Participación: <b>%{customdata[0]:.1f}%</b>"
            "<extra></extra>"
        ),
        pull=[0.03 if p == max(pcts) else 0 for p in pcts]
    ))

    layout = get_base_layout()
    layout.update(
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0",
                        font=dict(family="Inter", size=12, color="#1F2937")),
        annotations=[
            dict(font=dict(size=11, color='#94A3B8', family='Inter'),
                 showarrow=False, text="Total Tickets", x=0.5, y=0.55),
            dict(font=dict(size=18, color='#1E3A8A', family='Inter'),
                 showarrow=False, text=f"<b>{total:,}</b>", x=0.5, y=0.45)
        ]
    )
    fig.update_layout(**layout)
    return fig
