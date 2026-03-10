import polars as pl
import numpy as np
import json
import os
from jinja2 import Environment, FileSystemLoader

def generate_dashboard(input_path, output_path):
    print(f"Cargando datos desde {input_path}...")
    
    parquet_path = input_path.replace('.csv', '.parquet')
    
    if os.path.exists(parquet_path):
        print("Cargando desde cache Parquet...")
        dataframe_players = pl.read_parquet(parquet_path)
    else:
        print("Leyendo CSV y convirtiendo a Parquet...")
        try:
            dataframe_players = pl.read_csv(input_path, infer_schema_length=0) # Read all as string first for safety
        except Exception as e:
            try:
                dataframe_players = pl.read_csv(input_path, encoding='latin1', infer_schema_length=0)
            except Exception as e2:
                print("Error cargando el archivo:", e2)
                return

        # Clean column names
        dataframe_players = dataframe_players.rename({c: c.strip().lower() for c in dataframe_players.columns})
        
        # Type casting and filling nulls
        dataframe_players = dataframe_players.with_columns([
            pl.col("calculation_date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias("calculation_date")
        ])
        
        numeric_cols = ["ggr_usd", "amount_usd", "profit_usd", "odds", "deposits"]
        for c in numeric_cols:
            if c in dataframe_players.columns:
                dataframe_players = dataframe_players.with_columns(pl.col(c).cast(pl.Float64, strict=False).fill_null(0))
        
        if "username" in dataframe_players.columns:
            dataframe_players = dataframe_players.with_columns(pl.col("username").fill_null("Desconocido"))
        if "type_bet" in dataframe_players.columns:
            dataframe_players = dataframe_players.with_columns(
                pl.when(pl.col("type_bet").str.contains("(?i)sistema")).then(pl.lit("Sistema"))
                .when(pl.col("type_bet").str.contains("(?i)combinada|parlay")).then(pl.lit("Combinada"))
                .when(pl.col("type_bet").str.contains("(?i)simple")).then(pl.lit("Simple"))
                .when(pl.col("type_bet").str.contains("(?i)betbuilder|bet builder")).then(pl.lit("BetBuilder"))
                .otherwise(pl.lit("Otros"))
                .alias("type_bet")
            )
        if "status_bet" in dataframe_players.columns:
            dataframe_players = dataframe_players.with_columns(
                pl.when(pl.col("status_bet").str.contains("(?i)won|win|ganad")).then(pl.lit("Ganada"))
                .when(pl.col("status_bet").str.contains("(?i)lost|loss|perdid")).then(pl.lit("Perdido"))
                .when(pl.col("status_bet").str.contains("(?i)cashout|cash out")).then(pl.lit("CashOut"))
                .otherwise(pl.lit("Otro"))
                .alias("status_bet")
            )
        if "group_name" in dataframe_players.columns:
            dataframe_players = dataframe_players.with_columns(pl.col("group_name").fill_null("Sin Categoría"))
        else:
            dataframe_players = dataframe_players.with_columns(pl.lit("Sin Categoría").alias("group_name"))
            
        dataframe_players = dataframe_players.with_columns([
            pl.col("calculation_date").dt.strftime("%Y-%m").fill_null("Unknown").alias("month"),
            pl.col("calculation_date").dt.strftime("%Y-%m-%d").fill_null("Unknown").alias("date")
        ])
        
        dataframe_players = dataframe_players.with_columns(
            (pl.col("status_bet") == "Ganada").cast(pl.Int32).alias("won_flags")
        )

        print("Guardando cache Parquet...")
        dataframe_players.write_parquet(parquet_path)

    print("Pre-agregando datos para el dashboard...")
    
    # Global: Daily (Evolución Temporal)
    dataframe_daily = dataframe_players.group_by("date").agg([
        pl.col("ggr_usd").sum(),
        pl.col("amount_usd").sum(),
        pl.col("deposits").sum(),
        pl.col("withdrawal").sum()
    ]).sort("date").fill_null(0)

    # Global: Treemap y Rentabilidad y Eficiencia
    dataframe_segments = dataframe_players.group_by("group_name").agg([
        pl.col("ggr_usd").sum(),
        pl.col("deposits").sum(),
        pl.len().alias("_count"),
        pl.col("won_flags").sum()
    ]).fill_null(0).to_dicts()

    # Global: Riesgo de la Casa (House Profit)
    dataframe_house_risk = dataframe_players.group_by("type_bet").agg([
        (pl.when(pl.col("status_bet") == "Perdido").then(pl.col("amount_usd")).otherwise(0).sum() -
         pl.when(pl.col("status_bet") == "Ganada").then(pl.col("amount_usd")).otherwise(0).sum()).alias("profit")
    ]).fill_null(0).to_dicts()

    # Global: Odds Histograma
    odds_array = dataframe_players.filter(pl.col("odds") > 0).filter(pl.col("odds") < 50)["odds"].to_numpy()
    if len(odds_array) > 0:
        hist, bins = np.histogram(odds_array, bins=50)
        odds_distribution_data = {"bins": bins.tolist(), "values": [float(h) for h in hist]}
    else:
        odds_distribution_data = {"bins": [], "values": []}

    # Global: Top 10 Players
    dataframe_top_players = dataframe_players.group_by("username").agg([
        pl.col("ggr_usd").sum()
    ]).sort("ggr_usd", descending=True).head(10).to_dicts()

    top_usernames = [player["username"] for player in dataframe_top_players]

    # Player View (sólo para los Top 10 para no saturar el payload, < 1000 records)
    dataframe_top_players_rows = dataframe_players.filter(pl.col("username").is_in(top_usernames))
    
    players_data = {}
    for username in top_usernames:
        player_dataframe = dataframe_top_players_rows.filter(pl.col("username") == username)
        
        player_daily_data = player_dataframe.group_by("date").agg([
            pl.col("profit_usd").sum(),
            pl.col("deposits").sum()
        ]).sort("date").fill_null(0).to_dicts()
        
        player_turnover_data = player_dataframe.select([
            pl.col("deposits").sum(),
            pl.col("amount_usd").sum()
        ]).to_dicts()[0]
        
        # --- RISK PROFILE: breakdown by system × status ---
        player_risk_profile_data = player_dataframe.group_by(["type_bet", "status_bet"]).agg([
            pl.col("amount_usd").sum()
        ]).fill_null(0).rename({"type_bet": "system", "status_bet": "result"}).to_dicts()
        # ------------------------------------------
        
        player_preferences_data = player_dataframe.group_by("type_bet").agg([pl.col("amount_usd").sum(), pl.len().alias("_count")]).fill_null(0).to_dicts()
        player_ticket_statistics = player_dataframe.group_by("status_bet").agg([pl.len().alias("_count"), pl.col("ggr_usd").sum()]).fill_null(0).to_dicts()
        
        players_data[username] = {
            "daily": player_daily_data,
            "turnover": player_turnover_data,
            "risk": player_risk_profile_data,
            "preferences": player_preferences_data,
            "tickets": player_ticket_statistics
        }

    # Unique dimensions for dropdowns (solo para mantener la interfaz, aunque el filtrado activo cambió a estático por rendimiento)
    filter_months = dataframe_players["month"].unique().to_list()
    filter_groups = dataframe_players["group_name"].unique().to_list()

    print("Construyendo gráficos Plotly en backend...")
    import plotly
    import json
    
    from charts_python.chart_treemap_ggr import build_chart as build_treemap_chart
    from charts_python.chart_ggr_volume import build_chart as build_ggr_volume_chart
    from charts_python.chart_profit_vs_deposits import build_chart as build_profit_deposits_chart
    from charts_python.chart_house_risk import build_chart as build_house_risk_chart
    from charts_python.chart_odds_distribution import build_chart as build_odds_distribution_chart
    from charts_python.chart_efficiency_scatter import build_chart as build_efficiency_scatter_chart
    from charts_python.chart_top_players import build_chart as build_top_players_chart
    from charts_python.chart_winrate_heatmap import build_chart as build_winrate_heatmap_chart
    from charts_python.chart_withdrawals_vs_deposits import build_chart as build_withdrawals_vs_deposits_chart

    from charts_python.player_pnl import build_chart as build_player_pnl_chart
    from charts_python.player_turnover import build_chart as build_player_turnover_chart
    from charts_python.player_risk_profile import build_chart as build_player_risk_profile_chart
    from charts_python.player_preferences import build_chart as build_player_preferences_chart
    from charts_python.player_ticket_effectiveness import build_chart as build_player_ticket_effectiveness_chart

    def fig_to_dict(fig):
        return json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))

    # Convertir DFs necesarios que no se convirtieron en dicts previamente, o list->dicts
    segment_aggregation_dataframe = dataframe_players.group_by("group_name").agg([
        pl.col("ggr_usd").sum(), 
        pl.col("deposits").sum(), 
        pl.len().alias("_count"), 
        pl.col("won_flags").sum()
    ]).fill_null(0)

    figure_ggr_volume = build_ggr_volume_chart(dataframe_daily)
    figure_withdrawals = build_withdrawals_vs_deposits_chart(dataframe_daily)
    
    figure_treemap = build_treemap_chart(segment_aggregation_dataframe)
    figure_profit_deposits = build_profit_deposits_chart(segment_aggregation_dataframe)
    figure_winrate_heatmap = build_winrate_heatmap_chart(segment_aggregation_dataframe)
    figure_efficiency_scatter = build_efficiency_scatter_chart(segment_aggregation_dataframe)
    
    figure_house_risk = build_house_risk_chart(dataframe_house_risk)
    figure_odds_distribution = build_odds_distribution_chart(odds_distribution_data)
    
    figure_top_players = build_top_players_chart(
        dataframe_players.group_by("username").agg([pl.col("ggr_usd").sum()]).sort("ggr_usd", descending=True).head(10)
    )

    # Drill-down: per-segment scatter data (deposits vs GGR by user)
    segment_scatter_drilldown_data = {}
    for group_name in filter_groups:
        segment_dataframe = dataframe_players.filter(pl.col("group_name") == group_name).group_by("username").agg([
            pl.col("deposits").sum(), pl.col("ggr_usd").sum()
        ]).fill_null(0)
        segment_scatter_drilldown_data[group_name] = {
            "x": segment_dataframe["deposits"].to_list(),
            "y": segment_dataframe["ggr_usd"].to_list(),
            "text": segment_dataframe["username"].to_list()
        }

    encoded_players_charts = {}
    for username, player_data in players_data.items():
        if len(player_data["risk"]) > 0:
            print(f"Sample risk data for {username}: {player_data['risk'][:1]}")
            
        encoded_players_charts[username] = {
            "pnl": fig_to_dict(build_player_pnl_chart(player_data["daily"])),
            "turnover": fig_to_dict(build_player_turnover_chart(player_data["turnover"])),
            "risk": fig_to_dict(build_player_risk_profile_chart(player_data["risk"])),
            "preferences": fig_to_dict(build_player_preferences_chart(player_data["preferences"])),
            "tickets": fig_to_dict(build_player_ticket_effectiveness_chart(player_data["tickets"]))
        }

    payload = {
        "filters": {"months": filter_months, "groups": filter_groups, "players": top_usernames},
        "global_charts": {
            "ggr_volume": fig_to_dict(figure_ggr_volume),
            "treemap": fig_to_dict(figure_treemap),
            "profit_deposits": fig_to_dict(figure_profit_deposits),
            "house_risk": fig_to_dict(figure_house_risk),
            "odds_dist": fig_to_dict(figure_odds_distribution),
            "winrate": fig_to_dict(figure_winrate_heatmap),
            "eff_scatter": fig_to_dict(figure_efficiency_scatter),
            "top_players": fig_to_dict(figure_top_players),
            "withdrawals_vs_deposits": fig_to_dict(figure_withdrawals)
        },
        "segment_scatter": segment_scatter_drilldown_data,
        "players_charts": encoded_players_charts
    }

    json_payload = json.dumps(payload, allow_nan=False)

    size_kb = len(json_payload) / 1024
    print(f"Payload size: {size_kb:.2f} KB")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    template = env.get_template("dashboard.html")

    print("Generando HTML Dinámico y Alta Fidelidad...")
    html_output = template.render(json_payload=json_payload)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ Dashboard V4 (Light Mode Corporativo) guardado exitosamente en: {output_path}")

if __name__ == "__main__":
    generate_dashboard("data/data-1761320956212.csv", "reporte_jugadores.html")
