"""Altair chart functions for competitiveness visualization."""

import altair as alt
import polars as pl


def create_gini_trend_chart(
    gini_data: pl.DataFrame,
    season_col: str = "season",
    gini_col: str = "gini",
    title: str = "Points Inequality (Gini Coefficient) Over Time",
) -> alt.Chart:
    """Create a line chart showing Gini coefficient trend over seasons.

    Args:
        gini_data: DataFrame with season and gini columns
        season_col: Name of season column
        gini_col: Name of Gini coefficient column
        title: Chart title

    Returns:
        Altair Chart object
    """
    base = alt.Chart(gini_data).encode(
        x=alt.X(f"{season_col}:N", title="Season", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f"{gini_col}:Q", title="Gini Coefficient", scale=alt.Scale(domain=[0, 0.5])),
        tooltip=[
            alt.Tooltip(f"{season_col}:N", title="Season"),
            alt.Tooltip(f"{gini_col}:Q", title="Gini", format=".3f"),
        ],
    )

    line = base.mark_line(color="#1f77b4", strokeWidth=2)
    points = base.mark_circle(color="#1f77b4", size=60)

    return (
        (line + points)
        .properties(
            title=title,
            width=600,
            height=300,
        )
        .configure_title(
            fontSize=16,
            anchor="start",
        )
    )


def create_point_gaps_chart(
    gaps_data: pl.DataFrame,
    season_col: str = "season",
    title: str = "Point Gaps Over Time",
) -> alt.Chart:
    """Create a multi-line chart showing point gaps over seasons.

    Args:
        gaps_data: DataFrame with season, first_second, first_fourth, first_last columns
        season_col: Name of season column
        title: Chart title

    Returns:
        Altair Chart object
    """
    # Melt the data for Altair's multi-line format
    melted = gaps_data.unpivot(
        index=[season_col],
        on=["first_second", "first_fourth", "first_last"],
        variable_name="gap_type",
        value_name="points",
    )

    # Create readable labels
    label_mapping = {
        "first_second": "1st - 2nd (Title Race)",
        "first_fourth": "1st - 4th (UCL Spots)",
        "first_last": "1st - Last (Spread)",
    }

    melted = melted.with_columns(pl.col("gap_type").replace(label_mapping).alias("Gap Type"))

    chart = (
        alt.Chart(melted)
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X(f"{season_col}:N", title="Season", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("points:Q", title="Point Gap"),
            color=alt.Color(
                "Gap Type:N",
                scale=alt.Scale(
                    domain=list(label_mapping.values()),
                    range=["#e41a1c", "#377eb8", "#4daf4a"],
                ),
                legend=alt.Legend(title="Gap Type", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip(f"{season_col}:N", title="Season"),
                alt.Tooltip("Gap Type:N", title="Gap"),
                alt.Tooltip("points:Q", title="Points"),
            ],
        )
        .properties(
            title=title,
            width=600,
            height=300,
        )
        .configure_title(
            fontSize=16,
            anchor="start",
        )
    )

    return chart


def create_combined_metrics_chart(
    gini_data: pl.DataFrame,
    gaps_data: pl.DataFrame,
    season_col: str = "season",
) -> alt.VConcatChart:
    """Create a combined view of Gini and point gaps charts.

    Args:
        gini_data: DataFrame with season and gini columns
        gaps_data: DataFrame with season and point gap columns
        season_col: Name of season column

    Returns:
        Vertically concatenated Altair chart
    """
    gini_chart = create_gini_trend_chart(gini_data, season_col).properties(height=200)
    gaps_chart = create_point_gaps_chart(gaps_data, season_col).properties(height=200)

    return alt.vconcat(gini_chart, gaps_chart).resolve_scale(color="independent")


def create_gini_spread_chart(
    combined_data: pl.DataFrame,
    season_col: str = "season",
    gini_col: str = "gini",
    spread_col: str = "first_last",
    title: str = "Gini Coefficient vs League Spread",
) -> alt.LayerChart:
    """Create a dual Y-axis chart showing Gini and 1st-last spread together.

    Args:
        combined_data: DataFrame with season, gini, and first_last columns
        season_col: Name of season column
        gini_col: Name of Gini coefficient column
        spread_col: Name of first-last point gap column
        title: Chart title

    Returns:
        Layered Altair chart with dual Y-axes
    """
    base = alt.Chart(combined_data).encode(
        x=alt.X(f"{season_col}:N", title="Season", axis=alt.Axis(labelAngle=-45)),
    )

    gini_line = base.mark_line(color="steelblue", strokeWidth=2).encode(
        y=alt.Y(f"{gini_col}:Q", title="Gini Coefficient", axis=alt.Axis(titleColor="steelblue")),
        tooltip=[
            alt.Tooltip(f"{season_col}:N", title="Season"),
            alt.Tooltip(f"{gini_col}:Q", title="Gini", format=".3f"),
        ],
    )
    gini_points = base.mark_circle(color="steelblue", size=50).encode(
        y=alt.Y(f"{gini_col}:Q"),
    )

    spread_line = base.mark_line(color="orange", strokeWidth=2, strokeDash=[5, 5]).encode(
        y=alt.Y(
            f"{spread_col}:Q", title="1st-Last Gap (points)", axis=alt.Axis(titleColor="orange")
        ),
        tooltip=[
            alt.Tooltip(f"{season_col}:N", title="Season"),
            alt.Tooltip(f"{spread_col}:Q", title="1st-Last Gap"),
        ],
    )
    spread_points = base.mark_circle(color="orange", size=50).encode(
        y=alt.Y(f"{spread_col}:Q"),
    )

    return (
        alt.layer(gini_line, gini_points, spread_line, spread_points)
        .resolve_scale(y="independent")
        .properties(
            title=title,
            width=600,
            height=300,
        )
    )


def create_gini_and_gap_chart(
    combined_data: pl.DataFrame,
    season_col: str = "season",
    gini_col: str = "gini",
    spread_col: str = "gap",
    title: str = "Gini Coefficient and Grandes vs Pequenos Gap Over Time",
) -> alt.LayerChart:
    """Create a dual Y-axis chart showing Gini coefficient and grandes vs pequenos gap over seasons.

    Args:
        combined_data: DataFrame with season, gini, and gap columns (gap = grandes_avg - pequenos_avg)
        season_col: Name of season column
        gini_col: Name of Gini coefficient column
        spread_col: Name of grandes vs pequenos point gap column
        title: Chart title

    Returns:
        Layered Altair chart with dual Y-axes showing Gini (left) and gap (right)
    """
    base = alt.Chart(combined_data).encode(
        x=alt.X(f"{season_col}:N", title="Season", axis=alt.Axis(labelAngle=-45)),
    )

    gini_line = base.mark_line(color="steelblue", strokeWidth=2).encode(
        y=alt.Y(
            f"{gini_col}:Q",
            title="Gini Coefficient",
            axis=alt.Axis(titleColor="steelblue", orient="left"),
        ),
        tooltip=[
            alt.Tooltip(f"{season_col}:N", title="Season"),
            alt.Tooltip(f"{gini_col}:Q", title="Gini", format=".3f"),
        ],
    )
    gini_points = base.mark_circle(color="steelblue", size=50).encode(
        y=alt.Y(f"{gini_col}:Q", title="", axis=alt.Axis(orient="left")),
    )

    spread_line = base.mark_line(color="orange", strokeWidth=2, strokeDash=[5, 5]).encode(
        y=alt.Y(
            f"{spread_col}:Q",
            title="Gap Grandes Pequenos",
            axis=alt.Axis(titleColor="orange", orient="right"),
        ),
        tooltip=[
            alt.Tooltip(f"{season_col}:N", title="Season"),
            alt.Tooltip(f"{spread_col}:Q", title="Grandes vs Pequenos Gap", format=".1f"),
        ],
    )
    spread_points = base.mark_circle(color="orange", size=50).encode(
        y=alt.Y(f"{spread_col}:Q", title="Gap Grandes Pequenos", axis=alt.Axis(titleColor="orange", orient="right")),
    )

    return (
        alt.layer(gini_line, gini_points, spread_line, spread_points)
        .resolve_scale(y="independent")
        .properties(
            title=title,
            width=600,
            height=300,
        )
        .configure_title(
            fontSize=16,
            anchor="start",
        )
    )


def create_grandes_pequenos_chart(
    gp_data: pl.DataFrame,
    season_col: str = "season",
    title: str = "Grandes vs Pequenos Point Gap",
) -> alt.Chart:
    """Create a chart showing the gap between Big 3 and rest of league.

    Args:
        gp_data: DataFrame with season, grandes_avg, pequenos_avg, gap columns
        season_col: Name of season column
        title: Chart title

    Returns:
        Altair Chart showing the gap over time
    """
    # Create area chart showing both averages
    melted = gp_data.unpivot(
        index=[season_col],
        on=["grandes_avg", "pequenos_avg"],
        variable_name="group",
        value_name="avg_points",
    )

    label_mapping = {
        "grandes_avg": "Grandes (Benfica, Porto, Sporting)",
        "pequenos_avg": "Pequenos (Rest)",
    }

    melted = melted.with_columns(pl.col("group").replace(label_mapping).alias("Group"))

    lines = (
        alt.Chart(melted)
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X(f"{season_col}:N", title="Season", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("avg_points:Q", title="Average Points"),
            color=alt.Color(
                "Group:N",
                scale=alt.Scale(
                    domain=list(label_mapping.values()),
                    range=["#d62728", "#2ca02c"],
                ),
                legend=alt.Legend(title="Group", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip(f"{season_col}:N", title="Season"),
                alt.Tooltip("Group:N", title="Group"),
                alt.Tooltip("avg_points:Q", title="Avg Points", format=".1f"),
            ],
        )
        .properties(
            title=title,
            width=600,
            height=300,
        )
    )

    return lines
