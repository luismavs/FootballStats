"""Configuration dataclasses for league and analysis settings."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LeagueConfig:
    """Configuration for a football league.

    Attributes:
        name: Display name of the league (e.g., "Primeira Liga")
        soccerdata_key: Key used by soccerdata to identify the league
        fbref_id: FBref league ID for direct API access
        num_teams: Number of teams in the league
        champions_league_spots: Number of top positions qualifying for UCL
    """

    name: str
    soccerdata_key: str
    fbref_id: str
    num_teams: int = 18
    champions_league_spots: int = 4


@dataclass(frozen=True)
class AnalysisConfig:
    """Configuration for competitiveness analysis.

    Attributes:
        league: League configuration
        start_season: First season to analyze (e.g., "2014-2015")
        end_season: Last season to analyze (e.g., "2023-2024")
        seasons: List of season strings to analyze
    """

    league: LeagueConfig
    start_season: str
    end_season: str
    seasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Generate list of seasons if not provided."""
        if not self.seasons:
            start_year = int(self.start_season.split("-")[0])
            end_year = int(self.end_season.split("-")[0])
            seasons = [f"{year}-{year + 1}" for year in range(start_year, end_year + 1)]
            object.__setattr__(self, "seasons", seasons)


# Default configuration for Portuguese Primeira Liga
PRIMEIRA_LIGA = LeagueConfig(
    name="Primeira Liga",
    soccerdata_key="POR-Primeira Liga",
    fbref_id="32",
    num_teams=18,
    champions_league_spots=4,
)

DEFAULT_ANALYSIS = AnalysisConfig(
    league=PRIMEIRA_LIGA,
    start_season="2004-2005",
    end_season="2023-2024",
)
