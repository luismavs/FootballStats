"""Unit tests for point gap calculations."""

import polars as pl
import pytest

from football_competitiveness.metrics.point_gaps import (
    GRANDES,
    GrandesPequenosGap,
    PointGaps,
    calculate_all_grandes_pequenos_gaps,
    calculate_all_point_gaps,
    calculate_grandes_pequenos_gap,
    calculate_point_gaps,
    grandes_pequenos_to_dataframe,
    point_gaps_to_dataframe,
)


class TestPointGaps:
    """Tests for PointGaps dataclass."""

    def test_creation(self):
        """Should create PointGaps correctly."""
        gaps = PointGaps(first_second=5, first_fourth=15, first_last=50)
        assert gaps.first_second == 5
        assert gaps.first_fourth == 15
        assert gaps.first_last == 50
        assert gaps.season is None

    def test_creation_with_season(self):
        """Should create PointGaps with season."""
        gaps = PointGaps(first_second=5, first_fourth=15, first_last=50, season="2023-2024")
        assert gaps.season == "2023-2024"

    def test_immutable(self):
        """PointGaps should be immutable (frozen)."""
        gaps = PointGaps(first_second=5, first_fourth=15, first_last=50)
        with pytest.raises(AttributeError):
            gaps.first_second = 10


class TestCalculatePointGaps:
    """Tests for calculate_point_gaps function."""

    def test_basic_calculation(self, sample_standings):
        """Should calculate gaps correctly."""
        gaps = calculate_point_gaps(sample_standings)

        # From fixture: points = [80, 75, 70, 65, 40, 30]
        assert gaps.first_second == 5  # 80 - 75
        assert gaps.first_fourth == 15  # 80 - 65
        assert gaps.first_last == 50  # 80 - 30

    def test_extracts_season(self, sample_standings):
        """Should extract season from standings."""
        gaps = calculate_point_gaps(sample_standings)
        assert gaps.season == "2023-2024"

    def test_unsorted_input(self):
        """Should handle unsorted input with rank column."""
        df = pl.DataFrame({
            "rank": [3, 1, 4, 2],
            "points": [70, 90, 60, 80],
        })
        gaps = calculate_point_gaps(df)
        assert gaps.first_second == 10  # 90 - 80
        assert gaps.first_fourth == 30  # 90 - 60

    def test_close_competition(self):
        """Close standings should have small gaps."""
        df = pl.DataFrame({
            "rank": [1, 2, 3, 4],
            "points": [80, 79, 78, 77],
        })
        gaps = calculate_point_gaps(df)
        assert gaps.first_second == 1
        assert gaps.first_fourth == 3

    def test_missing_points_column_raises(self):
        """Missing points column should raise ValueError."""
        df = pl.DataFrame({"rank": [1, 2, 3, 4]})
        with pytest.raises(ValueError, match="not found"):
            calculate_point_gaps(df)

    def test_fewer_than_four_teams_raises(self):
        """Fewer than 4 teams should raise ValueError."""
        df = pl.DataFrame({
            "rank": [1, 2, 3],
            "points": [80, 70, 60],
        })
        with pytest.raises(ValueError, match="at least 4 teams"):
            calculate_point_gaps(df)

    def test_custom_points_column(self):
        """Should work with custom column name."""
        df = pl.DataFrame({
            "rank": [1, 2, 3, 4],
            "pts": [80, 70, 60, 50],
        })
        gaps = calculate_point_gaps(df, points_col="pts")
        assert gaps.first_second == 10
        assert gaps.first_fourth == 30


class TestCalculateAllPointGaps:
    """Tests for calculate_all_point_gaps function."""

    def test_multiple_seasons(self, multi_season_standings):
        """Should calculate gaps for each season."""
        gaps = calculate_all_point_gaps(multi_season_standings)

        assert len(gaps) == 2

        # Find gaps by season
        gaps_2022 = next(g for g in gaps if g.season == "2022-2023")
        gaps_2023 = next(g for g in gaps if g.season == "2023-2024")

        # 2022-2023: [80, 78, 76, 74] - more competitive
        assert gaps_2022.first_second == 2
        assert gaps_2022.first_fourth == 6

        # 2023-2024: [90, 70, 50, 30] - less competitive
        assert gaps_2023.first_second == 20
        assert gaps_2023.first_fourth == 60

    def test_missing_season_column_raises(self, sample_standings):
        """Missing season column should raise ValueError."""
        df = sample_standings.drop("season")
        with pytest.raises(ValueError, match="not found"):
            calculate_all_point_gaps(df)


class TestPointGapsToDataframe:
    """Tests for point_gaps_to_dataframe function."""

    def test_conversion(self):
        """Should convert list of PointGaps to DataFrame."""
        gaps = [
            PointGaps(5, 15, 50, "2022-2023"),
            PointGaps(10, 25, 60, "2023-2024"),
        ]
        df = point_gaps_to_dataframe(gaps)

        assert df.columns == ["season", "first_second", "first_fourth", "first_last"]
        assert df.height == 2
        assert df["season"].to_list() == ["2022-2023", "2023-2024"]
        assert df["first_second"].to_list() == [5, 10]
        assert df["first_fourth"].to_list() == [15, 25]
        assert df["first_last"].to_list() == [50, 60]

    def test_empty_list(self):
        """Should handle empty list."""
        df = point_gaps_to_dataframe([])
        assert df.height == 0
        assert df.columns == ["season", "first_second", "first_fourth", "first_last"]


class TestGrandesPequenosGap:
    """Tests for GrandesPequenosGap dataclass."""

    def test_creation(self):
        """Should create GrandesPequenosGap correctly."""
        gap = GrandesPequenosGap(grandes_avg=75.0, pequenos_avg=40.0, gap=35.0)
        assert gap.grandes_avg == 75.0
        assert gap.pequenos_avg == 40.0
        assert gap.gap == 35.0
        assert gap.season is None

    def test_creation_with_season(self):
        """Should create GrandesPequenosGap with season."""
        gap = GrandesPequenosGap(grandes_avg=75.0, pequenos_avg=40.0, gap=35.0, season="2023-2024")
        assert gap.season == "2023-2024"

    def test_immutable(self):
        """GrandesPequenosGap should be immutable (frozen)."""
        gap = GrandesPequenosGap(grandes_avg=75.0, pequenos_avg=40.0, gap=35.0)
        with pytest.raises(AttributeError):
            gap.gap = 40.0


class TestGrandesConstant:
    """Tests for GRANDES constant."""

    def test_contains_big_three(self):
        """Should contain the Big 3 Portuguese clubs."""
        assert "Benfica" in GRANDES
        assert "Porto" in GRANDES
        assert "Sporting CP" in GRANDES

    def test_has_three_teams(self):
        """Should have exactly 3 teams."""
        assert len(GRANDES) == 3


class TestCalculateGrandesPequenosGap:
    """Tests for calculate_grandes_pequenos_gap function."""

    def test_basic_calculation(self):
        """Should calculate gap correctly."""
        df = pl.DataFrame({
            "season": ["2023-2024"] * 6,
            "rank": [1, 2, 3, 4, 5, 6],
            "team": ["Benfica", "Porto", "Sporting CP", "Braga", "Vitória", "Nacional"],
            "points": [80, 75, 70, 50, 40, 30],
        })
        gap = calculate_grandes_pequenos_gap(df)

        # Grandes avg: (80 + 75 + 70) / 3 = 75
        # Pequenos avg: (50 + 40 + 30) / 3 = 40
        assert gap.grandes_avg == pytest.approx(75.0)
        assert gap.pequenos_avg == pytest.approx(40.0)
        assert gap.gap == pytest.approx(35.0)

    def test_extracts_season(self):
        """Should extract season from standings."""
        df = pl.DataFrame({
            "season": ["2023-2024"] * 4,
            "team": ["Benfica", "Porto", "Sporting CP", "Braga"],
            "points": [80, 75, 70, 50],
        })
        gap = calculate_grandes_pequenos_gap(df)
        assert gap.season == "2023-2024"

    def test_missing_points_column_raises(self):
        """Missing points column should raise ValueError."""
        df = pl.DataFrame({
            "team": ["Benfica", "Porto", "Sporting CP", "Braga"],
        })
        with pytest.raises(ValueError, match="not found"):
            calculate_grandes_pequenos_gap(df)

    def test_missing_team_column_raises(self):
        """Missing team column should raise ValueError."""
        df = pl.DataFrame({
            "points": [80, 75, 70, 50],
        })
        with pytest.raises(ValueError, match="not found"):
            calculate_grandes_pequenos_gap(df)


class TestCalculateAllGrandesPequenosGaps:
    """Tests for calculate_all_grandes_pequenos_gaps function."""

    def test_multiple_seasons(self):
        """Should calculate gaps for each season."""
        df = pl.DataFrame({
            "season": ["2022-2023"] * 4 + ["2023-2024"] * 4,
            "team": ["Benfica", "Porto", "Sporting CP", "Braga"] * 2,
            "points": [80, 78, 76, 40, 90, 85, 80, 50],
        })
        gaps = calculate_all_grandes_pequenos_gaps(df)

        assert len(gaps) == 2

        gap_2022 = next(g for g in gaps if g.season == "2022-2023")
        gap_2023 = next(g for g in gaps if g.season == "2023-2024")

        # 2022-2023: Grandes avg = (80+78+76)/3 = 78, Pequenos avg = 40
        assert gap_2022.grandes_avg == pytest.approx(78.0)
        assert gap_2022.pequenos_avg == pytest.approx(40.0)
        assert gap_2022.gap == pytest.approx(38.0)

        # 2023-2024: Grandes avg = (90+85+80)/3 = 85, Pequenos avg = 50
        assert gap_2023.grandes_avg == pytest.approx(85.0)
        assert gap_2023.pequenos_avg == pytest.approx(50.0)
        assert gap_2023.gap == pytest.approx(35.0)

    def test_missing_season_column_raises(self):
        """Missing season column should raise ValueError."""
        df = pl.DataFrame({
            "team": ["Benfica", "Porto"],
            "points": [80, 75],
        })
        with pytest.raises(ValueError, match="not found"):
            calculate_all_grandes_pequenos_gaps(df)


class TestGrandesPequenosToDataframe:
    """Tests for grandes_pequenos_to_dataframe function."""

    def test_conversion(self):
        """Should convert list of GrandesPequenosGap to DataFrame."""
        gaps = [
            GrandesPequenosGap(75.0, 40.0, 35.0, "2022-2023"),
            GrandesPequenosGap(80.0, 45.0, 35.0, "2023-2024"),
        ]
        df = grandes_pequenos_to_dataframe(gaps)

        assert df.columns == ["season", "grandes_avg", "pequenos_avg", "gap"]
        assert df.height == 2
        assert df["season"].to_list() == ["2022-2023", "2023-2024"]
        assert df["grandes_avg"].to_list() == [75.0, 80.0]
        assert df["pequenos_avg"].to_list() == [40.0, 45.0]
        assert df["gap"].to_list() == [35.0, 35.0]

    def test_empty_list(self):
        """Should handle empty list."""
        df = grandes_pequenos_to_dataframe([])
        assert df.height == 0
        assert df.columns == ["season", "grandes_avg", "pequenos_avg", "gap"]
