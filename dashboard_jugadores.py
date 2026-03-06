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
        df = pl.read_parquet(parquet_path)
    else:
        print("Leyendo CSV y convirtiendo a Parquet...")
        try:
            df = pl.read_csv(input_path, infer_schema_length=0) # Read all as string first for safety
        except Exception as e:
            try:
                df = pl.read_csv(input_path, encoding='latin1', infer_schema_length=0)
            except Exception as e2:
                print("Error cargando el archivo:", e2)
                return

        # Clean column names
        df = df.rename({c: c.strip().lower() for c in df.columns})
        
        # Type casting and filling nulls
        df = df.with_columns([
            pl.col("calculation_date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias("calculation_date")
        ])
        
        numeric_cols = ["ggr_usd", "amount_usd", "profit_usd", "odds", "deposits"]
        for c in numeric_cols:
            if c in df.columns:
                df = df.with_columns(pl.col(c).cast(pl.Float64, strict=False).fill_null(0))
        
        if "username" in df.columns:
            df = df.with_columns(pl.col("username").fill_null("Desconocido"))
        if "type_bet" in df.columns:
            df = df.with_columns(
                pl.when(pl.col("type_bet").str.contains("(?i)sistema")).then(pl.lit("Sistema"))
                .when(pl.col("type_bet").str.contains("(?i)combinada|parlay")).then(pl.lit("Combinada"))
                .when(pl.col("type_bet").str.contains("(?i)simple")).then(pl.lit("Simple"))
                .when(pl.col("type_bet").str.contains("(?i)betbuilder|bet builder")).then(pl.lit("BetBuilder"))
                .otherwise(pl.lit("Otros"))
                .alias("type_bet")
            )
        if "status_bet" in df.columns:
            df = df.with_columns(
                pl.when(pl.col("status_bet").str.contains("(?i)won|win|ganad")).then(pl.lit("Ganada"))
                .when(pl.col("status_bet").str.contains("(?i)lost|loss|perdid")).then(pl.lit("Perdido"))
                .when(pl.col("status_bet").str.contains("(?i)cashout|cash out")).then(pl.lit("CashOut"))
                .otherwise(pl.lit("Otro"))
                .alias("status_bet")
            )
        if "group_name" in df.columns:
            df = df.with_columns(pl.col("group_name").fill_null("Sin Categoría"))
        else:
            df = df.with_columns(pl.lit("Sin Categoría").alias("group_name"))
            
        df = df.with_columns([
            pl.col("calculation_date").dt.strftime("%Y-%m").fill_null("Unknown").alias("month"),
            pl.col("calculation_date").dt.strftime("%Y-%m-%d").fill_null("Unknown").alias("date")
        ])
        
        df = df.with_columns(
            (pl.col("status_bet") == "Ganada").cast(pl.Int32).alias("won_flags")
        )

        print("Guardando cache Parquet...")
        df.write_parquet(parquet_path)

    print("Pre-agregando datos para el dashboard...")
    
    # Global: Daily (Evolución Temporal)
    df_daily = df.group_by("date").agg([
        pl.col("ggr_usd").sum(),
        pl.col("amount_usd").sum(),
        pl.col("deposits").sum()
    ]).sort("date").fill_null(0)

    # Global: Treemap y Rentabilidad y Eficiencia
    df_segments = df.group_by("group_name").agg([
        pl.col("ggr_usd").sum(),
        pl.col("deposits").sum(),
        pl.len().alias("_count"),
        pl.col("won_flags").sum()
    ]).fill_null(0).to_dicts()

    # Global: Riesgo de la Casa (House Profit)
    df_house_risk = df.group_by("type_bet").agg([
        (pl.when(pl.col("status_bet") == "Perdido").then(pl.col("amount_usd")).otherwise(0).sum() -
         pl.when(pl.col("status_bet") == "Ganada").then(pl.col("amount_usd")).otherwise(0).sum()).alias("profit")
    ]).fill_null(0).to_dicts()

    # Global: Odds Histograma
    odds_array = df.filter(pl.col("odds") > 0).filter(pl.col("odds") < 50)["odds"].to_numpy()
    if len(odds_array) > 0:
        hist, bins = np.histogram(odds_array, bins=50)
        odds_hist = {"bins": bins.tolist(), "values": [float(h) for h in hist]}
    else:
        odds_hist = {"bins": [], "values": []}

    # Global: Top 10 Players
    df_top_players = df.group_by("username").agg([
        pl.col("ggr_usd").sum()
    ]).sort("ggr_usd", descending=True).head(10).to_dicts()

    top_usernames = [p["username"] for p in df_top_players]

    # Player View (sólo para los Top 10 para no saturar el payload, < 1000 records)
    # Si desean ver un jugador, la data ya está aquí para los más relevantes
    df_top_rows = df.filter(pl.col("username").is_in(top_usernames))
    
    players_data = {}
    for username in top_usernames:
        df_p = df_top_rows.filter(pl.col("username") == username)
        p_daily = df_p.group_by("date").agg([
            pl.col("profit_usd").sum(),
            pl.col("deposits").sum()
        ]).sort("date").fill_null(0).to_dicts()
        
        p_turnover = df_p.select([
            pl.col("deposits").sum(),
            pl.col("amount_usd").sum()
        ]).to_dicts()[0]
        
        # --- RISK PROFILE: breakdown by system × status ---
        df_p_risk = df_p.group_by(["type_bet", "status_bet"]).agg([
            pl.col("amount_usd").sum()
        ]).fill_null(0).rename({"type_bet": "system", "status_bet": "result"}).to_dicts()
        # ------------------------------------------
        
        p_pref = df_p.group_by("type_bet").agg([pl.col("amount_usd").sum(), pl.len().alias("_count")]).fill_null(0).to_dicts()
        p_ticket = df_p.group_by("status_bet").agg([pl.len().alias("_count")]).fill_null(0).to_dicts()
        
        players_data[username] = {
            "daily": p_daily,
            "turnover": p_turnover,
            "risk": df_p_risk,
            "preferences": p_pref,
            "tickets": p_ticket
        }

    # Unique dimensions for dropdowns (solo para mantener la interfaz, aunque el filtrado activo cambió a estático por rendimiento)
    months = df["month"].unique().to_list()
    groups = df["group_name"].unique().to_list()

    print("Construyendo gráficos Plotly en backend...")
    import plotly
    import json
    from charts_python.chart_treemap_ggr import build_chart as b_treemap
    from charts_python.chart_ggr_volume import build_chart as b_ggr_volume
    from charts_python.chart_profit_vs_deposits import build_chart as b_profit_dep
    from charts_python.chart_house_risk import build_chart as b_house_risk
    from charts_python.chart_odds_distribution import build_chart as b_odds_dist
    from charts_python.chart_efficiency_scatter import build_chart as b_eff_scatter
    from charts_python.chart_top_players import build_chart as b_top_players
    from charts_python.chart_winrate_heatmap import build_chart as b_winrate
    from charts_python.chart_withdrawals_vs_deposits import build_chart as b_withdrawals

    from charts_python.player_pnl import build_chart as b_pnl
    from charts_python.player_turnover import build_chart as b_turnover
    from charts_python.player_risk_profile import build_chart as b_risk
    from charts_python.player_preferences import build_chart as b_pref
    from charts_python.player_ticket_effectiveness import build_chart as b_ticket

    def fig_to_dict(fig):
        return json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))

    # Convertir DFs necesarios que no se convirtieron en dicts previamente, o list->dicts
    fig_ggr_volume = b_ggr_volume(df_daily)
    fig_withdrawals = b_withdrawals(df_daily)
    fig_treemap = b_treemap(df.group_by("group_name").agg([pl.col("ggr_usd").sum(), pl.col("deposits").sum(), pl.len().alias("_count"), pl.col("won_flags").sum()]).fill_null(0))
    fig_profit_dep = b_profit_dep(df.group_by("group_name").agg([pl.col("ggr_usd").sum(), pl.col("deposits").sum(), pl.len().alias("_count"), pl.col("won_flags").sum()]).fill_null(0))
    fig_house_risk = b_house_risk(df_house_risk)
    fig_odds_dist = b_odds_dist(odds_hist)
    fig_winrate = b_winrate(df.group_by("group_name").agg([pl.col("ggr_usd").sum(), pl.col("deposits").sum(), pl.len().alias("_count"), pl.col("won_flags").sum()]).fill_null(0))
    fig_eff_scatter = b_eff_scatter(df.group_by("group_name").agg([pl.col("ggr_usd").sum(), pl.col("deposits").sum(), pl.len().alias("_count"), pl.col("won_flags").sum()]).fill_null(0))
    fig_top_players = b_top_players(df.group_by("username").agg([pl.col("ggr_usd").sum()]).sort("ggr_usd", descending=True).head(10))

    # Drill-down: per-segment scatter data (deposits vs GGR by user)
    segment_scatter_data = {}
    for gn in groups:
        df_seg = df.filter(pl.col("group_name") == gn).group_by("username").agg([
            pl.col("deposits").sum(), pl.col("ggr_usd").sum()
        ]).fill_null(0)
        segment_scatter_data[gn] = {
            "x": df_seg["deposits"].to_list(),
            "y": df_seg["ggr_usd"].to_list(),
            "text": df_seg["username"].to_list()
        }

    players_charts = {}
    for uname, pdata in players_data.items():
        # Debugging print to verify data structure
        if len(pdata["risk"]) > 0:
            print(f"Sample risk data for {uname}: {pdata['risk'][:1]}")
            
        players_charts[uname] = {
            "pnl": fig_to_dict(b_pnl(pdata["daily"])),
            "turnover": fig_to_dict(b_turnover(pdata["turnover"])),
            "risk": fig_to_dict(b_risk(pdata["risk"])),
            "preferences": fig_to_dict(b_pref(pdata["preferences"])),
            "tickets": fig_to_dict(b_ticket(pdata["tickets"]))
        }

    payload = {
        "filters": {"months": months, "groups": groups, "players": top_usernames},
        "global_charts": {
            "ggr_volume": fig_to_dict(fig_ggr_volume),
            "treemap": fig_to_dict(fig_treemap),
            "profit_deposits": fig_to_dict(fig_profit_dep),
            "house_risk": fig_to_dict(fig_house_risk),
            "odds_dist": fig_to_dict(fig_odds_dist),
            "winrate": fig_to_dict(fig_winrate),
            "eff_scatter": fig_to_dict(fig_eff_scatter),
            "top_players": fig_to_dict(fig_top_players),
            "withdrawals_vs_deposits": fig_to_dict(fig_withdrawals)
        },
        "segment_scatter": segment_scatter_data,
        "players_charts": players_charts
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
