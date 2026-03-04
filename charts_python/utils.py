import plotly.graph_objects as go

paleta_corpo = {
    "royalBlue": "#1E3A8A",
    "emerald": "#10B981",
    "crimson": "#E11D48",
    "teal": "#0D9488",
    "amber": "#F59E0B",
    "sky500": "#0EA5E9",
    "slate": "#64748B"
}

def get_base_layout():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#475569'),
        margin=dict(t=40, r=10, l=50, b=30),
        title=None
    )
