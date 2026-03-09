import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(df_top_players):
    # 1. Validación de datos
    if len(df_top_players) == 0:
        return go.Figure()
        
    # 2. Ordenamiento de datos
    df = df_top_players.sort("ggr_usd", descending=False)
    
    # 3. Declaración de variables
    ggr_values = df["ggr_usd"].to_list()
    player_usernames = df["username"].to_list()
    text_values = [f"${v:,.0f}" for v in ggr_values]

    # 4. Configuración de colores corporativos
    bar_color_primary = "#1E3A8A"   # Royal Blue
    bar_color_negative = "#E11D48"  # Crimson
    grid_color = "#F1F5F9"
    margin_layout = dict(t=0, b=20, l=120, r=10)

    bar_colors = [bar_color_primary if v >= 0 else bar_color_negative for v in ggr_values]

    # 5. Construcción del gráfico
    hover_template = 'Jugador: %{y}<br>GGR: $%{x:,.2f}<extra></extra>'

    horizontal_bar_trace = go.Bar(
        x=ggr_values,
        y=player_usernames,
        orientation='h',
        marker=dict(
            color=bar_colors,
            opacity=1.0
        ),
        text=text_values,
        textposition='inside',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate=hover_template
    )
    
    figure_object = go.Figure(horizontal_bar_trace)

    # 6. Configuración de layout
    chart_layout = get_base_layout()
    chart_layout.update(
        height=380,
        margin=margin_layout,
        yaxis=dict(
            showgrid=False, 
            zeroline=False, 
            automargin=True
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor=grid_color, 
            zeroline=False, 
            tickformat='$,.0s'
        ),
        hoverlabel=dict(
            bgcolor="white", 
            bordercolor="#E2E8F0", 
            font=dict(family="Inter", color="#1F2937")
        )
    )
    figure_object.update_layout(**chart_layout)

    # 7. Render final
    return figure_object
