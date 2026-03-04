import plotly.graph_objects as go
from charts_python.utils import paleta_corpo, get_base_layout

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()
        
    x_vals = df_segments["group_name"].to_list()
    won = df_segments["won_flags"].to_list()
    count = df_segments["_count"].to_list()
    
    wr = [ (w/c * 100) if c > 0 else 0 for w, c in zip(won, count) ]
    z_data = [wr]
    
    texto = [[f"{v:.1f}%" for v in wr]]

    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_vals,
        y=['WR %'],
        colorscale=[[0, '#FFFFFF'], [1, paleta_corpo["emerald"]]],
        showscale=False,
        text=texto,
        texttemplate='%{text}',
        hovertemplate='<b>WR:</b> %{z:.2f}%<extra></extra>'
    ))

    layout = get_base_layout()
    layout.update(margin=dict(t=10, b=30, l=40, r=10))
    fig.update_layout(**layout)
    return fig
