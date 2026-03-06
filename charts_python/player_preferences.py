import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

# Color mapping with corporate hierarchy
_COLORS = {
    "Combinada": paleta_corpo["royalBlue"],
    "Simple": paleta_corpo["teal"],
    "BetBuilder": "#94A3B8",
    "Otros": "#CBD5E1"
}

def build_chart(p_pref):
    if not p_pref:
        return go.Figure()

    labels = [d["type_bet"] for d in p_pref]
    values = [d["amount_usd"] for d in p_pref]
    counts = [d.get("_count", 0) for d in p_pref]
    colors = [_COLORS.get(l, "#CBD5E1") for l in labels]

    tot_apo = sum(values)
    tot_count = sum(counts)

    # Only show label for dominant segment
    pcts = [(v / tot_apo * 100) if tot_apo > 0 else 0 for v in values]
    text_info = [f"{labels[i]}<br>{pcts[i]:.1f}%" if pcts[i] > 15 else "" for i in range(len(labels))]

    # Custom data for tooltips
    custom = list(zip(pcts, counts))

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='text', text=text_info,
        textfont=dict(size=12, color='white', family='Inter'),
        customdata=custom,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "──────────<br>"
            "Monto apostado: <b>$%{value:,.0f}</b><br>"
            "Participación: <b>%{customdata[0]:.1f}%</b><br>"
            "Apuestas realizadas: <b>%{customdata[1]:,}</b>"
            "<extra></extra>"
        ),
        pull=[0.03 if p == max(pcts) else 0 for p in pcts]
    ))

    layout = get_base_layout()
    layout.update(
        autosize=True,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(orientation='h', y=-0.05, x=0.5, xanchor='center',
                    font=dict(size=11, color='#64748b', family='Inter')),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0",
                        font=dict(family="Inter", size=12, color="#1F2937")),
        annotations=[
            dict(font=dict(size=11, color='#94A3B8', family='Inter'),
                 showarrow=False, text="Total Apostado", x=0.5, y=0.55),
            dict(font=dict(size=18, color='#1E3A8A', family='Inter', weight='bold' if hasattr(dict, '__class__') else None),
                 showarrow=False, text=f"<b>${tot_apo:,.0f}</b>", x=0.5, y=0.45)
        ]
    )
    fig.update_layout(**layout)
    return fig
