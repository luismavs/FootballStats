"""Football Competitiveness Analysis package."""

from football_competitiveness.config import AnalysisConfig, LeagueConfig
from football_competitiveness.metrics.gini import gini_coefficient, gini_from_standings
from football_competitiveness.metrics.point_gaps import PointGaps, calculate_point_gaps

__all__ = [
    "AnalysisConfig",
    "LeagueConfig",
    "gini_coefficient",
    "gini_from_standings",
    "PointGaps",
    "calculate_point_gaps",
]
