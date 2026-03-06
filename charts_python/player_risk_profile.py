import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_risk):
    if not p_risk:
        return go.Figure()

    # Data: [{system, result, amount_usd}, ...]
    systems = sorted(list(set(d["system"] for d in p_risk)))
    results_order = ["Perdido", "CashOut", "Ganada"]
    colors = {"Ganada": paleta_corpo["emerald"], "Perdido": paleta_corpo["crimson"], "CashOut": paleta_corpo["amber"]}
    labels = {"Ganada": "Ganado", "Perdido": "Perdido", "CashOut": "CashOut"}

    # Totals per system for percentage calculation
    sys_totals = {}
    for d in p_risk:
        sys_totals[d["system"]] = sys_totals.get(d["system"], 0) + d["amount_usd"]

    fig = go.Figure()

    for res in results_order:
        data_res = [d for d in p_risk if d.get("result") == res]
        if not data_res:
            continue

        y_vals = []
        custom = []
        for sys in systems:
            val = next((d["amount_usd"] for d in data_res if d["system"] == sys), 0)
            y_vals.append(val)
            pct = (val / sys_totals[sys] * 100) if sys_totals.get(sys, 0) > 0 else 0
            custom.append(f"{pct:.0f}%")

        fig.add_trace(go.Bar(
            name=labels.get(res, res), x=systems, y=y_vals,
            marker=dict(color=colors.get(res, paleta_corpo["slate"])),
            customdata=custom,
            hovertemplate=(
                "<b>Sistema:</b> %{x}<br>"
                "<b>Resultado:</b> " + labels.get(res, res) + "<br>"
                "<b>Exposición:</b> $%{y:,.0f}<br>"
                "<b>Participación:</b> %{customdata}<extra></extra>"
            )
        ))

    layout = get_base_layout()
    layout.update(
        autosize=True, barmode='stack', bargap=0.3,
        margin=dict(l=50, r=20, t=40, b=50),
        xaxis=dict(title="Sistema de Juego", showgrid=False,
                   tickfont=dict(size=11, color='#475569', family='Inter')),
        yaxis=dict(title="Exposición (USD)", tickprefix='$', tickformat=',.0f',
                   gridcolor='rgba(0,0,0,0.05)', zeroline=False,
                   tickfont=dict(size=11, color='#64748b', family='Inter')),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0",
                        font=dict(family="Inter", size=12, color="#1F2937")),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center',
                    font=dict(size=11, color='#64748b'))
    )
    fig.update_layout(**layout)
    return fig
