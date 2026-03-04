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
        }
    } else {
        if (playerView) playerView.classList.remove('active');
        if (globalView) {
            setTimeout(() => globalView.classList.add('active'), 50);
            renderGlobalView(dashboardData.global_charts);
        }
    }
}

function renderGlobalView(global_charts) {
    if (!global_charts) return;

    renderPlotlyChart('gl-chart-1', global_charts.ggr_volume);

    // Plotly needs an empty container for top players since it was originally a table wrapper
    const topCont = document.querySelector('.top-table-container');
    if (topCont && topCont.querySelector('table')) {
        topCont.innerHTML = '<div id="gl-chart-8" class="plot-container"></div>';
    }

    renderPlotlyChart('gl-chart-2', global_charts.treemap);
    renderPlotlyChart('gl-chart-3', global_charts.profit_deposits);
    renderPlotlyChart('gl-chart-4', global_charts.house_risk);
    renderPlotlyChart('gl-chart-5', global_charts.odds_dist);
    renderPlotlyChart('gl-chart-6', global_charts.winrate);
    renderPlotlyChart('gl-chart-7', global_charts.eff_scatter);
    renderPlotlyChart('gl-chart-8', global_charts.top_players);
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
