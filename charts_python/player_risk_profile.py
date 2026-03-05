import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_risk):
    if not p_risk:
        return go.Figure()
        
    # Datos: {system, result, amount_usd}
    # Agrupar datos para Stacked Bar
    systems = sorted(list(set(d["system"] for d in p_risk)))
    results_order = ["Ganado", "Perdido", "CashOut"]
    colors = {"Ganado": "emerald", "Perdido": "crimson", "CashOut": "amber"}
    
    fig = go.Figure()

    for res in results_order:
        # Filtrar datos por resultado
        data_res = [d for d in p_risk if d.get("result") == res]
        if not data_res: continue
            
        # Mapear montos por sistema
        y_vals = []
        for sys in systems:
            val = next((d["amount_usd"] for d in data_res if d["system"] == sys), 0)
            y_vals.append(val)
            
        fig.add_trace(go.Bar(
            name=res,
            x=systems,
            y=y_vals,
            marker_color=paleta_corpo.get(colors[res], paleta_corpo["royalBlue"]),
            hovertemplate=(
                "Sistema: <b>%{x}</b><br>" +
                "Monto: <b>$%{y:,.2f}</b><br>" +
                "Resultado: <b>%{legendgroup}</b><extra></extra>"
            ),
            legendgroup=res
        ))

    layout = get_base_layout()
    layout.update(
        barmode='stack',
        xaxis=dict(title='Sistema de Juego'),
        yaxis=dict(title='Exposición (USD)'),
        margin=dict(l=40, r=20, t=30, b=40),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font=dict(family="Inter", color="#1F2937")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_layout(**layout)
    return fig
