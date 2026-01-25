"""Data fetcher for league standings data."""

from pathlib import Path

import polars as pl

from football_competitiveness.config import AnalysisConfig, DEFAULT_ANALYSIS


class StandingsFetcher:
    """Fetches football standings data from bundled CSV files.

    This class loads historical league standings from CSV files bundled
    with the package.

    Attributes:
        config: Analysis configuration specifying league and seasons
    """

    def __init__(self, config: AnalysisConfig | None = None) -> None:
        """Initialize the fetcher with analysis configuration.

        Args:
            config: Analysis configuration. Defaults to Portuguese Primeira Liga.
        """
        self.config = config or DEFAULT_ANALYSIS
        self._data: pl.DataFrame | None = None

    @property
    def data_path(self) -> Path:
        """Path to the standings CSV file."""
        return Path(__file__).parent.parent.parent.parent / "data" / "primeira_liga_standings.csv"

    def _load_data(self) -> pl.DataFrame:
        """Load and cache the standings data."""
        if self._data is None:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Standings data not found at {self.data_path}")

            self._data = pl.read_csv(self.data_path)

        return self._data

    def fetch_standings(self, season: str | None = None) -> pl.DataFrame:
        """Fetch league standings for a season or all configured seasons.

        Args:
            season: Specific season to fetch (e.g., "2023-2024").
                   If None, fetches all configured seasons.

        Returns:
            Polars DataFrame with columns:
                - season: Season string (e.g., "2023-2024")
                - rank: Final league position (1 = champion)
                - team: Team name
                - points: Total points
                - matches: Matches played
                - wins: Number of wins
                - draws: Number of draws
                - losses: Number of losses
                - goals_for: Goals scored
                - goals_against: Goals conceded
                - goal_difference: Goal difference
        """
        data = self._load_data()

        if season:
            return data.filter(pl.col("season") == season)

        # Filter to configured seasons
        return data.filter(pl.col("season").is_in(self.config.seasons))

    def fetch_all_standings(self) -> pl.DataFrame:
        """Fetch standings for all configured seasons.

        Returns:
            Polars DataFrame with standings for all seasons combined.
        """
        return self.fetch_standings(season=None)

    def get_season_points(self, season: str) -> pl.Series:
        """Get just the points column for a specific season.

        Args:
            season: Season to fetch (e.g., "2023-2024")

        Returns:
            Polars Series of points, sorted by rank (1st place first)
        """
        standings = self.fetch_standings(season)
        return standings.sort("rank")["points"]


# Alias for backwards compatibility
FBrefFetcher = StandingsFetcher
