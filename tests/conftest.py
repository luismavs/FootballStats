"""Pytest fixtures for football-competitiveness tests."""

import polars as pl
import pytest


@pytest.fixture
def sample_standings() -> pl.DataFrame:
    """Sample standings data for a single season."""
    return pl.DataFrame({
        "season": ["2023-2024"] * 6,
        "rank": [1, 2, 3, 4, 5, 6],
        "team": ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F"],
        "points": [80, 75, 70, 65, 40, 30],
        "matches": [34] * 6,
        "wins": [25, 22, 20, 18, 10, 7],
        "draws": [5, 9, 10, 11, 10, 9],
        "losses": [4, 3, 4, 5, 14, 18],
        "goals_for": [75, 68, 62, 55, 40, 35],
        "goals_against": [30, 35, 40, 45, 60, 70],
        "goal_difference": [45, 33, 22, 10, -20, -35],
    })


@pytest.fixture
def multi_season_standings() -> pl.DataFrame:
    """Sample standings data for multiple seasons."""
    seasons_data = []

    # Season 2022-2023: More competitive
    seasons_data.append(pl.DataFrame({
        "season": ["2022-2023"] * 4,
        "rank": [1, 2, 3, 4],
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "points": [80, 78, 76, 74],
    }))

    # Season 2023-2024: Less competitive
    seasons_data.append(pl.DataFrame({
        "season": ["2023-2024"] * 4,
        "rank": [1, 2, 3, 4],
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "points": [90, 70, 50, 30],
    }))

    return pl.concat(seasons_data)


@pytest.fixture
def equal_points_standings() -> pl.DataFrame:
    """Standings where all teams have equal points (Gini = 0)."""
    return pl.DataFrame({
        "season": ["2023-2024"] * 4,
        "rank": [1, 2, 3, 4],
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "points": [50, 50, 50, 50],
    })


@pytest.fixture
def unequal_points_standings() -> pl.DataFrame:
    """Standings with high inequality."""
    return pl.DataFrame({
        "season": ["2023-2024"] * 4,
        "rank": [1, 2, 3, 4],
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "points": [100, 10, 5, 1],
    })
