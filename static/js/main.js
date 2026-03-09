let dashboardData = {};

document.addEventListener('DOMContentLoaded', () => {
    try {
        const scriptData = document.getElementById('dashboard-data');
        if (scriptData) {
            dashboardData = JSON.parse(scriptData.textContent);
            console.log('Dashboard Data Loaded (Plotly Python Figs):', dashboardData);
            initDashboard();
        }
    } catch (e) {
        console.error('Error parsing dashboard data:', e);
    }
});

function initDashboard() {
    renderGlobalView(dashboardData.global_charts);

    if (dashboardData.filters && dashboardData.filters.players && dashboardData.filters.players.length > 0) {
        const firstPlayer = dashboardData.filters.players[0];
        initPlayerSelect(dashboardData.filters.players, firstPlayer);
    }

    // Filtros deshabilitados
    const monthFilterElement = document.getElementById('filter-month');
    const groupFilterElement = document.getElementById('filter-group_name');
    if (monthFilterElement) { monthFilterElement.disabled = true; monthFilterElement.title = "Filtro deshabilitado: Datos optimizados a nivel global"; }
    if (groupFilterElement) { groupFilterElement.disabled = true; groupFilterElement.title = "Filtro deshabilitado: Datos optimizados a nivel global"; }

    document.getElementById('btn-reset').addEventListener('click', () => {
        const sel = document.getElementById('filter-player');
        if (sel) sel.value = 'ALL';
        updateDashboard();
    });
}

function updateDashboard() {
    const playerFilterDropdown = document.getElementById('filter-player');
    const selectedPlayer = playerFilterDropdown ? playerFilterDropdown.value : 'ALL';
    const globalViewContainer = document.getElementById('global-view');
    const playerViewContainer = document.getElementById('player-view');

    if (selectedPlayer !== 'ALL' && dashboardData.players_charts && dashboardData.players_charts[selectedPlayer]) {
        if (globalViewContainer) globalViewContainer.classList.remove('active');
        if (playerViewContainer) {
            setTimeout(() => playerViewContainer.classList.add('active'), 50);
            const playerViewTitle = document.getElementById('pv-title');
            if (playerViewTitle) playerViewTitle.innerText = `Vista de Jugador: ${selectedPlayer}`;
            renderPlayerView(selectedPlayer);
            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        }
    } else {
        if (playerViewContainer) playerViewContainer.classList.remove('active');
        if (globalViewContainer) {
            setTimeout(() => globalViewContainer.classList.add('active'), 50);
            renderGlobalView(dashboardData.global_charts);
            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        }
    }
}

function renderGlobalView(global_charts) {
    if (!global_charts) return;

    renderPlotlyChart('gl-chart-1', global_charts.ggr_volume);

    renderPlotlyChart('gl-chart-2', global_charts.treemap);
    renderPlotlyChart('gl-chart-3', global_charts.profit_deposits);
    renderPlotlyChart('gl-chart-4', global_charts.house_risk);
    renderPlotlyChart('gl-chart-5', global_charts.odds_dist);
    renderPlotlyChart('gl-chart-6', global_charts.winrate);
    renderPlotlyChart('gl-chart-7', global_charts.eff_scatter);
    renderPlotlyChart('gl-chart-8', global_charts.top_players);
    renderPlotlyChart('withdrawals_vs_deposits_chart', global_charts.withdrawals_vs_deposits);

    // Drill-down: click on efficiency scatter to explore segment detail
    const efficiencyScatterPlot = document.getElementById('gl-chart-7');
    if (efficiencyScatterPlot && dashboardData.segment_scatter) {
        efficiencyScatterPlot.on('plotly_click', function (data) {
            const segmentName = data.points[0].text;
            const segmentScatterData = dashboardData.segment_scatter[segmentName];
            if (!segmentScatterData) return;

            const pointColors = segmentScatterData.y.map(ggr => {
                if (ggr > 0) return '#1E3A8A';
                if (ggr < 0) return '#E11D48';
                return '#94A3B8';
            });

            const drillFig = {
                data: [{
                    x: segmentScatterData.x, y: segmentScatterData.y, text: segmentScatterData.text,
                    mode: 'markers',
                    marker: { size: 6, color: pointColors, opacity: 0.85, line: { color: 'white', width: 1.0 } },
                    hovertemplate: '<b>%{text}</b><br>Depósitos: <b>$%{x:,.0f}</b><br>GGR: <b>$%{y:,.0f}</b><extra></extra>'
                }],
                layout: Object.assign({}, global_charts.eff_scatter.layout, {
                    annotations: [{
                        x: 0.5, y: 1.05, xref: 'paper', yref: 'paper',
                        text: '<b>Segmento: ' + segmentName + '</b>  (doble click para volver)',
                        showarrow: false, font: { size: 13, color: '#1E3A8A' }
                    }],
                    shapes: []
                })
            };
            renderPlotlyChart('gl-chart-7', drillFig);
        });

        efficiencyScatterPlot.on('plotly_doubleclick', function () {
            renderPlotlyChart('gl-chart-7', global_charts.eff_scatter);
        });
    }
}

function renderPlayerView(username) {
    if (!dashboardData.players_charts || !dashboardData.players_charts[username]) return;

    const playerChartsData = dashboardData.players_charts[username];

    renderPlotlyChart('pl-chart-1', playerChartsData.pnl);
    renderPlotlyChart('pl-chart-2', playerChartsData.risk);
    renderPlotlyChart('pl-chart-3', playerChartsData.preferences);
    renderPlotlyChart('pl-chart-4', playerChartsData.tickets);
    renderPlotlyChart('pl-chart-5', playerChartsData.turnover);
}

function initPlayerSelect(players, defaultPlayer) {
    const sel = document.getElementById('filter-player');
    if (!sel) return;

    // Preserve the first "ALL" option
    const options = `<option value="ALL">Buscar Jugador...</option>` + players.map(p => `<option value="${p}">${p}</option>`).join('');
    sel.innerHTML = options;
    sel.value = 'ALL';

    sel.addEventListener('change', updateDashboard);
}

function resetTreemap() {
    if (dashboardData.global_charts) {
        renderPlotlyChart('gl-chart-2', dashboardData.global_charts.treemap);
    }
}

function resetEfficiencyScatter() {
    if (dashboardData.global_charts) {
        renderPlotlyChart('gl-chart-7', dashboardData.global_charts.eff_scatter);
    }
}
