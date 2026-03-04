import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout
import polars as pl

def build_chart(df_house_risk):
    if len(df_house_risk) == 0:
        return go.Figure()
        
    # pivot df to get Won, Lost, Cashout per type_bet
    pivoted = df_house_risk.pivot(values="_count", index="type_bet", on="status_bet").fill_null(0)
    
    x_vals = pivoted["type_bet"].to_list()
    won = pivoted["Won"].to_list() if "Won" in pivoted.columns else [0]*len(x_vals)
    lost = pivoted["Lost"].to_list() if "Lost" in pivoted.columns else [0]*len(x_vals)
    cashout = pivoted["Cashout"].to_list() if "Cashout" in pivoted.columns else [0]*len(x_vals)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_vals, y=lost, name='Perdido',
        marker=dict(color=paleta_corpo["crimson"], line=dict(width=0)),
        hovertemplate='<b>Perdido:</b> %{y}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=x_vals, y=won, name='Ganado',
        marker=dict(color=paleta_corpo["emerald"], line=dict(width=0)),
        hovertemplate='<b>Ganado:</b> %{y}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=x_vals, y=cashout, name='CashOut',
        marker=dict(color=paleta_corpo["amber"], line=dict(width=0)),
        hovertemplate='<b>CashOut:</b> %{y}<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(barmode='stack')
    fig.update_layout(**layout)
    return fig
