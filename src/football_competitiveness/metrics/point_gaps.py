"""Point gap calculations for measuring competitiveness."""

from dataclasses import dataclass

import polars as pl

# The "Big 3" Portuguese clubs
GRANDES = {"Benfica", "Porto", "Sporting CP"}


@dataclass(frozen=True)
class PointGaps:
    """Point gaps between positions in the standings.

    Attributes:
        first_second: Gap between 1st and 2nd place (title race)
        first_fourth: Gap between 1st and 4th place (UCL qualification)
        first_last: Gap between 1st and last place (overall spread)
        season: Optional season identifier
    """

    first_second: int
    first_fourth: int
    first_last: int
    season: str | None = None


def calculate_point_gaps(standings: pl.DataFrame, points_col: str = "points") -> PointGaps:
    """Calculate point gaps from standings.

    Args:
        standings: DataFrame with standings data, must have rank and points columns.
                  Expected to be sorted by rank or contain a 'rank' column.
        points_col: Name of the column containing points

    Returns:
        PointGaps dataclass with gap values

    Raises:
        ValueError: If standings has fewer than 4 teams or missing columns
    """
    if points_col not in standings.columns:
        raise ValueError(f"Column '{points_col}' not found in standings")

    # Sort by rank if available, otherwise assume already sorted by position
    if "rank" in standings.columns:
        sorted_standings = standings.sort("rank")
    else:
        sorted_standings = standings

    n_teams = sorted_standings.height
    if n_teams < 4:
        raise ValueError(f"Standings must have at least 4 teams, got {n_teams}")

    points = sorted_standings[points_col].to_list()

    # Extract season if available
    season = None
    if "season" in standings.columns:
        seasons = standings["season"].unique()
        if len(seasons) == 1:
            season = str(seasons[0])

    return PointGaps(
        first_second=points[0] - points[1],
        first_fourth=points[0] - points[3],
        first_last=points[0] - points[-1],
        season=season,
    )


def calculate_all_point_gaps(
    standings: pl.DataFrame,
    points_col: str = "points",
    season_col: str = "season",
) -> list[PointGaps]:
    """Calculate point gaps for multiple seasons.

    Args:
        standings: DataFrame with standings for multiple seasons
        points_col: Name of the column containing points
        season_col: Name of the column containing season identifiers

    Returns:
        List of PointGaps, one per season
    """
    if season_col not in standings.columns:
        raise ValueError(f"Column '{season_col}' not found in standings")

    results = []
    for season in standings[season_col].unique().sort():
        season_standings = standings.filter(pl.col(season_col) == season)
        gaps = calculate_point_gaps(season_standings, points_col)
        # Create new PointGaps with season set
        results.append(PointGaps(
            first_second=gaps.first_second,
            first_fourth=gaps.first_fourth,
            first_last=gaps.first_last,
            season=str(season),
        ))

    return results


def point_gaps_to_dataframe(gaps: list[PointGaps]) -> pl.DataFrame:
    """Convert list of PointGaps to a Polars DataFrame.

    Args:
        gaps: List of PointGaps dataclasses

    Returns:
        DataFrame with columns: season, first_second, first_fourth, first_last
    """
    return pl.DataFrame({
        "season": [g.season for g in gaps],
        "first_second": [g.first_second for g in gaps],
        "first_fourth": [g.first_fourth for g in gaps],
        "first_last": [g.first_last for g in gaps],
    })


@dataclass(frozen=True)
class GrandesPequenosGap:
    """Gap between the Big 3 (Grandes) and other teams (Pequenos).

    Attributes:
        grandes_avg: Average points of Benfica, Porto, Sporting CP
        pequenos_avg: Average points of all other teams
        gap: Difference (grandes_avg - pequenos_avg)
        season: Optional season identifier
    """

    grandes_avg: float
    pequenos_avg: float
    gap: float
    season: str | None = None


def calculate_grandes_pequenos_gap(
    standings: pl.DataFrame,
    points_col: str = "points",
    team_col: str = "team",
) -> GrandesPequenosGap:
    """Calculate the gap between Big 3 average points and rest of league.

    Args:
        standings: DataFrame with standings data for a single season
        points_col: Name of the column containing points
        team_col: Name of the column containing team names

    Returns:
        GrandesPequenosGap with average points and gap

    Raises:
        ValueError: If required columns are missing
    """
    if points_col not in standings.columns:
        raise ValueError(f"Column '{points_col}' not found in standings")
    if team_col not in standings.columns:
        raise ValueError(f"Column '{team_col}' not found in standings")

    grandes = standings.filter(pl.col(team_col).is_in(GRANDES))
    pequenos = standings.filter(~pl.col(team_col).is_in(GRANDES))

    grandes_avg = grandes[points_col].mean()
    pequenos_avg = pequenos[points_col].mean()

    # Extract season if available
    season = None
    if "season" in standings.columns:
        seasons = standings["season"].unique()
        if len(seasons) == 1:
            season = str(seasons[0])

    return GrandesPequenosGap(
        grandes_avg=float(grandes_avg) if grandes_avg is not None else 0.0,
        pequenos_avg=float(pequenos_avg) if pequenos_avg is not None else 0.0,
        gap=float(grandes_avg - pequenos_avg) if grandes_avg is not None and pequenos_avg is not None else 0.0,
        season=season,
    )


def calculate_all_grandes_pequenos_gaps(
    standings: pl.DataFrame,
    points_col: str = "points",
    team_col: str = "team",
    season_col: str = "season",
) -> list[GrandesPequenosGap]:
    """Calculate Grandes vs Pequenos gaps for multiple seasons.

    Args:
        standings: DataFrame with standings for multiple seasons
        points_col: Name of the column containing points
        team_col: Name of the column containing team names
        season_col: Name of the column containing season identifiers

    Returns:
        List of GrandesPequenosGap, one per season
    """
    if season_col not in standings.columns:
        raise ValueError(f"Column '{season_col}' not found in standings")

    results = []
    for season in standings[season_col].unique().sort():
        season_standings = standings.filter(pl.col(season_col) == season)
        gap = calculate_grandes_pequenos_gap(season_standings, points_col, team_col)
        results.append(GrandesPequenosGap(
            grandes_avg=gap.grandes_avg,
            pequenos_avg=gap.pequenos_avg,
            gap=gap.gap,
            season=str(season),
        ))

    return results


def grandes_pequenos_to_dataframe(gaps: list[GrandesPequenosGap]) -> pl.DataFrame:
    """Convert list of GrandesPequenosGap to a Polars DataFrame.

    Args:
        gaps: List of GrandesPequenosGap dataclasses

    Returns:
        DataFrame with columns: season, grandes_avg, pequenos_avg, gap
    """
    return pl.DataFrame({
        "season": [g.season for g in gaps],
        "grandes_avg": [g.grandes_avg for g in gaps],
        "pequenos_avg": [g.pequenos_avg for g in gaps],
        "gap": [g.gap for g in gaps],
    })
