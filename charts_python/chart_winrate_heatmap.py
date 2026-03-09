# 1. Imports
import plotly.graph_objects as go
from charts_python.utils import get_base_layout

def build_chart(df_segments):
    # 2. Validación de datos
    if len(df_segments) == 0:
        return go.Figure()
        
    # 3. Preparación de datos
    segment_names = df_segments["group_name"].to_list()
    total_winning_tickets = df_segments["won_flags"].to_list()
    total_tickets = df_segments["_count"].to_list()
    
    # 4. Cálculo de métricas
    win_rate_percentage = [
        (won / total * 100) if total > 0 else 0 
        for won, total in zip(total_winning_tickets, total_tickets)
    ]
    heatmap_values = [win_rate_percentage]
    heatmap_labels = [[f"<b>{rate:.1f}%</b>" for rate in win_rate_percentage]]

    # 5. Configuración de visualización
    heatmap_colorscale = [
        [0.0, "#E2E8F0"],  # Bajo rendimiento (Slate Blue claro)
        [0.5, "#94A3B8"],  # Rendimiento medio (Slate Blue)
        [1.0, "#1E3A8A"]   # Alto rendimiento (Royal Blue)
    ]
    hover_template = '<b>WR:</b> %{z:.2f}%<extra></extra>'

    # 6. Construcción del gráfico
    heatmap_trace = go.Heatmap(
        z=heatmap_values,
        x=segment_names,
        y=['WR %'],
        colorscale=heatmap_colorscale,
        showscale=False,
        text=heatmap_labels,
        texttemplate='%{text}',
        hovertemplate=hover_template
    )
    
    figure_object = go.Figure(data=heatmap_trace)

    # 7. Configuración de layout
    chart_layout = get_base_layout()
    chart_layout.update(
        margin=dict(t=10, b=30, l=40, r=10)
    )
    figure_object.update_layout(**chart_layout)
    
    # 8. Return del gráfico
    return figure_object
