function renderPlotlyChart(containerId, fig) {
    if (!fig || !fig.data) {
        console.warn(`No figure data provided for ${containerId}`);
        return;
    }

    const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false
    };

    Plotly.react(
        containerId,
        fig.data,
        fig.layout,
        config
    );
}
