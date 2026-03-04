import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_ticket):
    if not p_ticket:
        return go.Figure()
        
    cm = {'won': paleta_corpo["emerald"], 'lost': paleta_corpo["crimson"], 'cashout': '#38BDF8'}
    
    labels = [d["status_bet"] for d in p_ticket]
    values = [d["_count"] for d in p_ticket]
    
    c_arr = []
    for lbl in labels:
        s = str(lbl).lower()
        color = '#CBD5E1'
        for k, v in cm.items():
            if k in s:
                color = v
                break
        c_arr.append(color)

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        marker=dict(colors=c_arr),
        hovertemplate='%{label}: %{value} tickets<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False
    )
    fig.update_layout(**layout)
    return fig
