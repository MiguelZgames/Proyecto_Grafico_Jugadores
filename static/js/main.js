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
    const mF = document.getElementById('filter-month');
    const gF = document.getElementById('filter-group_name');
    if (mF) { mF.disabled = true; mF.title = "Filtro deshabilitado: Datos optimizados a nivel global"; }
    if (gF) { gF.disabled = true; gF.title = "Filtro deshabilitado: Datos optimizados a nivel global"; }

    document.getElementById('btn-reset').addEventListener('click', () => {
        const sel = document.getElementById('filter-player');
        if (sel) sel.value = 'ALL';
        updateDashboard();
    });
}

function updateDashboard() {
    const playerFilter = document.getElementById('filter-player');
    const sp = playerFilter ? playerFilter.value : 'ALL';
    const globalView = document.getElementById('global-view');
    const playerView = document.getElementById('player-view');

    if (sp !== 'ALL' && dashboardData.players_charts && dashboardData.players_charts[sp]) {
        if (globalView) globalView.classList.remove('active');
        if (playerView) {
            setTimeout(() => playerView.classList.add('active'), 50);
            const pvTitle = document.getElementById('pv-title');
            if (pvTitle) pvTitle.innerText = `Vista de Jugador: ${sp}`;
            renderPlayerView(sp);
            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        }
    } else {
        if (playerView) playerView.classList.remove('active');
        if (globalView) {
            setTimeout(() => globalView.classList.add('active'), 50);
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
    const effPlot = document.getElementById('gl-chart-7');
    if (effPlot && dashboardData.segment_scatter) {
        effPlot.on('plotly_click', function (data) {
            const segment = data.points[0].text;
            const segData = dashboardData.segment_scatter[segment];
            if (!segData) return;

            const drillFig = {
                data: [{
                    x: segData.x, y: segData.y, text: segData.text,
                    mode: 'markers',
                    marker: { size: 10, color: '#2563EB', opacity: 0.7, line: { color: 'white', width: 1.5 } },
                    hovertemplate: '<b>%{text}</b><br>Depósitos: <b>$%{x:,.0f}</b><br>GGR: <b>$%{y:,.0f}</b><extra></extra>'
                }],
                layout: Object.assign({}, global_charts.eff_scatter.layout, {
                    annotations: [{
                        x: 0.5, y: 1.05, xref: 'paper', yref: 'paper',
                        text: '<b>Segmento: ' + segment + '</b>  (doble click para volver)',
                        showarrow: false, font: { size: 13, color: '#1E3A8A' }
                    }],
                    shapes: []
                })
            };
            renderPlotlyChart('gl-chart-7', drillFig);
        });

        effPlot.on('plotly_doubleclick', function () {
            renderPlotlyChart('gl-chart-7', global_charts.eff_scatter);
        });
    }
}

function renderPlayerView(username) {
    if (!dashboardData.players_charts || !dashboardData.players_charts[username]) return;

    const pc = dashboardData.players_charts[username];

    renderPlotlyChart('pl-chart-1', pc.pnl);
    renderPlotlyChart('pl-chart-2', pc.risk);
    renderPlotlyChart('pl-chart-3', pc.preferences);
    renderPlotlyChart('pl-chart-4', pc.tickets);
    renderPlotlyChart('pl-chart-5', pc.turnover);
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
