import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(mo):
    mo.md("""
    # How competitive is Primeira Liga?

    This notebook analyzes the competitiveness of the Portuguese Primeira Liga
    over the past 20 seasons (2004-2024) using:

    - **Gini Coefficient**: Measures inequality in final points (0 = equal, 1 = unequal)
    - **Point Gaps**: Tracks gaps between 1st-2nd, 1st-4th, and 1st-last positions
    - **Grandes vs Pequenos**: Gap between Big 3 (Benfica, Porto, Sporting) and rest of league
    """)
    return


@app.cell
def _():
    from football_competitiveness.config import DEFAULT_ANALYSIS, AnalysisConfig
    from football_competitiveness.data.fetcher import FBrefFetcher
    from football_competitiveness.metrics.gini import gini_from_standings
    from football_competitiveness.metrics.point_gaps import (
        calculate_all_point_gaps,
        calculate_all_grandes_pequenos_gaps,
        grandes_pequenos_to_dataframe,
        point_gaps_to_dataframe,
    )
    from football_competitiveness.visualization.charts import (
        create_gini_trend_chart,
        create_gini_spread_chart,
        create_grandes_pequenos_chart,
        create_point_gaps_chart,
        create_gini_and_gap_chart
    )
    return (
        AnalysisConfig,
        DEFAULT_ANALYSIS,
        FBrefFetcher,
        calculate_all_grandes_pequenos_gaps,
        calculate_all_point_gaps,
        create_gini_and_gap_chart,
        create_gini_trend_chart,
        create_grandes_pequenos_chart,
        create_point_gaps_chart,
        gini_from_standings,
        grandes_pequenos_to_dataframe,
        point_gaps_to_dataframe,
    )


@app.cell
def _(mo):
    mo.md("""
    ## Configuration
    """)
    return


@app.cell
def _(DEFAULT_ANALYSIS, mo):
    # Season selector
    available_seasons = DEFAULT_ANALYSIS.seasons
    season_selector = mo.ui.multiselect(
        options=available_seasons,
        value=available_seasons,
        label="Select Seasons",
    )
    season_selector
    return (season_selector,)


@app.cell
def _(mo, season_selector):
    mo.stop(len(season_selector.value) == 0, mo.md("**Please select at least one season.**"))
    return


@app.cell
def _(mo):
    mo.md("""
    ## Data Loading
    """)
    return


@app.cell
def _(AnalysisConfig, DEFAULT_ANALYSIS, FBrefFetcher, mo, pl, season_selector):
    # Create config with selected seasons
    selected_config = AnalysisConfig(
        league=DEFAULT_ANALYSIS.league,
        start_season=season_selector.value[0],# ty:ignore[invalid-argument-type]
        end_season=season_selector.value[-1],# ty:ignore[invalid-argument-type]
        seasons=list(season_selector.value),  # ty:ignore[invalid-argument-type]
    )

    with mo.status.spinner("Fetching standings data from FBref..."):
        try:
            fetcher = FBrefFetcher(selected_config)
            standings = fetcher.fetch_all_standings()
            data_status = mo.md(f"✓ Loaded {standings.height} team-season records")
        except Exception as e:
            standings = pl.DataFrame()
            data_status = mo.md(f"**Error loading data:** {e}")

    data_status
    return (standings,)


@app.cell
def _(mo, standings):
    mo.stop(standings.is_empty(), mo.md("**No data available. Check your connection and try again.**"))
    return


@app.cell
def _(mo):
    mo.md("""
    ## Standings Data
    """)
    return


@app.cell
def _(mo, standings):
    mo.ui.table(standings, selection=None, pagination=True)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Competitiveness Metrics
    """)
    return


@app.cell
def _(gini_from_standings, pl, standings):
    # Calculate Gini coefficient per season
    gini_results = []
    for season in standings["season"].unique().sort():
        season_data = standings.filter(pl.col("season") == season)
        gini = gini_from_standings(season_data)
        gini_results.append({"season": season, "gini": gini})

    gini_df = pl.DataFrame(gini_results)
    return (gini_df,)


@app.cell
def _(calculate_all_point_gaps, point_gaps_to_dataframe, standings):
    # Calculate point gaps per season
    gaps = calculate_all_point_gaps(standings)
    gaps_df = point_gaps_to_dataframe(gaps)
    return (gaps_df,)


@app.cell
def _(mo):
    mo.md("""
    ### Gini Coefficient Trend
    """)
    return


@app.cell
def _(create_gini_trend_chart, gini_df, mo):
    gini_chart = create_gini_trend_chart(gini_df)
    mo.ui.altair_chart(gini_chart)
    return


@app.cell
def _(gini_df, mo):
    avg_gini = gini_df["gini"].mean()
    min_gini = gini_df["gini"].min()
    max_gini = gini_df["gini"].max()

    mo.md(
        f"""
        **Summary Statistics:**
        - Average Gini: **{avg_gini:.3f}**
        - Range: {min_gini:.3f} - {max_gini:.3f}

        *Lower values indicate more competitive leagues (more equal point distribution).*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ### Point Gaps Trend
    """)
    return


@app.cell
def _(create_point_gaps_chart, gaps_df, mo):
    gaps_chart = create_point_gaps_chart(gaps_df)
    mo.ui.altair_chart(gaps_chart)
    return


@app.cell
def _(gaps_df, mo):
    avg_title_gap = gaps_df["first_second"].mean()
    avg_ucl_gap = gaps_df["first_fourth"].mean()

    mo.md(
        f"""
        **Summary Statistics:**
        - Average title race gap (1st-2nd): **{avg_title_gap:.1f} points**
        - Average UCL qualification gap (1st-4th): **{avg_ucl_gap:.1f} points**

        *Smaller gaps indicate more competitive title races and qualification battles.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Raw Metrics Data
    """)
    return


@app.cell
def _(gaps_df, gini_df, mo):
    # Join metrics for combined view
    combined_metrics = gini_df.join(gaps_df, on="season", how="inner")
    mo.ui.table(combined_metrics, selection=None)
    return (combined_metrics,)


@app.cell
def _(mo):
    mo.md("""
    ## Grandes vs Pequenos

    Comparing the average points of the "Big 3" (Benfica, Porto, Sporting CP) against
    all other teams in the league.
    """)
    return


@app.cell
def _(
    calculate_all_grandes_pequenos_gaps,
    grandes_pequenos_to_dataframe,
    standings,
):
    # Calculate Grandes vs Pequenos gaps per season
    gp_gaps = calculate_all_grandes_pequenos_gaps(standings)
    gp_df = grandes_pequenos_to_dataframe(gp_gaps)
    return (gp_df,)


@app.cell
def _(create_grandes_pequenos_chart, gp_df, mo):
    gp_chart = create_grandes_pequenos_chart(gp_df)
    mo.ui.altair_chart(gp_chart)
    return


@app.cell
def _(gp_df, mo):
    avg_gap = gp_df["gap"].mean()
    min_gap = gp_df["gap"].min()
    max_gap = gp_df["gap"].max()

    mo.md(
        f"""
        **Summary Statistics:**
        - Average gap (Grandes - Pequenos): **{avg_gap:.1f} points**
        - Range: {min_gap:.1f} - {max_gap:.1f} points

        *A larger gap indicates greater dominance by the Big 3 clubs.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Combined View: Gini & Grandes vs Pequenos Gap

    Dual-axis chart showing both the Gini coefficient (inequality measure) and the
    gap between Grandes (Big 3) and Pequenos (rest of league) over time.
    """)
    return


@app.cell
def _(create_gini_and_gap_chart, gini_df, gp_df, mo):
    # Combine Gini and Grandes vs Pequenos gap data
    gini_gap_combined = gini_df.join(gp_df, on="season", how="inner")
    spread_chart = create_gini_and_gap_chart(gini_gap_combined)
    mo.ui.altair_chart(spread_chart)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
