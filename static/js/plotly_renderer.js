function renderPlotlyChart(containerId, fig) {
    if (!fig || !fig.data) {
        console.warn(`No figure data provided for ${containerId}`);
        return;
    }

    const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false,
        doubleClick: 'reset'
    };

    const container = document.getElementById(containerId);
    if (!container) return;

    // Limpiar estado previo para evitar herencia de layout/escalas
    Plotly.purge(container);
    Plotly.newPlot(containerId, fig.data, fig.layout, config);
}
