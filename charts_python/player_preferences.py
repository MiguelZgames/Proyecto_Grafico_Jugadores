import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(p_pref):
    if not p_pref:
        return go.Figure()
        
    labels = [d["type_bet"] for d in p_pref]
    values = [d["amount_usd"] for d in p_pref]
    
    tot_apo = sum(values)
    main_kpi = f"${int(tot_apo):,}"

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.7,
        textinfo='label+percent',
        marker=dict(colors=[paleta_corpo["royalBlue"], paleta_corpo["teal"], '#38BDF8', '#94A3B8']),
        hovertemplate='%{label}<br>$%{value:,.2f}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        annotations=[dict(font=dict(size=16, color='#2D3748'), showarrow=False, text=main_kpi, x=0.5, y=0.5)]
    )
    fig.update_layout(**layout)
    return fig
