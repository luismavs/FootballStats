"""Competitiveness metrics module."""

from football_competitiveness.metrics.gini import gini_coefficient, gini_from_standings
from football_competitiveness.metrics.point_gaps import (
    GRANDES,
    GrandesPequenosGap,
    PointGaps,
    calculate_all_grandes_pequenos_gaps,
    calculate_grandes_pequenos_gap,
    calculate_point_gaps,
    grandes_pequenos_to_dataframe,
)

__all__ = [
    "GRANDES",
    "GrandesPequenosGap",
    "PointGaps",
    "calculate_all_grandes_pequenos_gaps",
    "calculate_grandes_pequenos_gap",
    "calculate_point_gaps",
    "gini_coefficient",
    "gini_from_standings",
    "grandes_pequenos_to_dataframe",
]
