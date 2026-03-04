import plotly.graph_objects as go

def build_chart(df_segments):
    if len(df_segments) == 0:
        return go.Figure()

    df = df_segments.filter(df_segments["ggr_usd"] > 0).sort("ggr_usd", descending=True)
    total = df["ggr_usd"].sum()

    colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
    fmt = lambda v: f'${v/1e6:.1f}M' if v>=1e6 else (f'${v/1e3:.1f}K' if v>=1e3 else f'${v:,.0f}')

    labels, values = df["group_name"].to_list(), df["ggr_usd"].to_list()
    text = [f"{g}<br>{fmt(v)}<br>{(v/total)*100:.1f}%" for g, v in zip(labels, values)]

    fig = go.Figure(go.Treemap(
        branchvalues="total",
        labels=["Global"] + labels,
        parents=[""] + ["Global"] * len(labels),
        values=[total] + values,
        text=["Global"] + text,
        texttemplate="<b>%{text}</b>",
        textfont=dict(color="white", size=14, family="Inter"),
        marker=dict(colors=["white"] + [colors[i % len(colors)] for i in range(len(labels))], line=dict(width=1.5, color="white")),
        hovertemplate="<b>%{label}</b><br>GGR: <b>$%{value:,.0f}</b><br>Share: <b>%{percentParent:.1%}</b><extra></extra>"
    ))

    fig.update_layout(
        height=520, margin=dict(t=0, l=0, r=0, b=0),
        uniformtext=dict(mode="hide", minsize=11),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", align="left", namelength=-1)
    )

    return fig