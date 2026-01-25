"""Unit tests for Gini coefficient calculations."""

import numpy as np
import polars as pl
import pytest

from football_competitiveness.metrics.gini import gini_coefficient, gini_from_standings


class TestGiniCoefficient:
    """Tests for gini_coefficient function."""

    def test_perfect_equality(self):
        """All equal values should give Gini = 0."""
        values = [50, 50, 50, 50]
        assert gini_coefficient(values) == pytest.approx(0.0)

    def test_perfect_equality_larger(self):
        """Larger array with equal values should still give Gini = 0."""
        values = [100] * 20
        assert gini_coefficient(values) == pytest.approx(0.0)

    def test_maximum_inequality_two_values(self):
        """One has everything, one has nothing -> Gini = 0.5 for n=2."""
        # For n=2: [0, 100] -> Gini = 0.5
        values = [0, 100]
        result = gini_coefficient(values)
        assert result == pytest.approx(0.5)

    def test_high_inequality(self):
        """High inequality should give high Gini."""
        values = [100, 1, 1, 1]
        result = gini_coefficient(values)
        assert result > 0.5

    def test_moderate_inequality(self):
        """Typical standings should give moderate Gini."""
        # Realistic league standings
        values = [80, 75, 70, 65, 60, 55, 50, 45, 40, 35]
        result = gini_coefficient(values)
        assert 0.05 < result < 0.3

    def test_numpy_array_input(self):
        """Should work with numpy arrays."""
        values = np.array([80, 70, 60, 50])
        result = gini_coefficient(values)
        assert 0 < result < 1

    def test_polars_series_input(self):
        """Should work with Polars Series."""
        values = pl.Series([80, 70, 60, 50])
        result = gini_coefficient(values)
        assert 0 < result < 1

    def test_empty_array_raises(self):
        """Empty array should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            gini_coefficient([])

    def test_negative_values_raises(self):
        """Negative values should raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            gini_coefficient([50, 40, -10, 20])

    def test_all_zeros(self):
        """All zeros should return 0 (all equal)."""
        values = [0, 0, 0, 0]
        assert gini_coefficient(values) == pytest.approx(0.0)

    def test_single_value(self):
        """Single value should return 0."""
        values = [50]
        assert gini_coefficient(values) == pytest.approx(0.0)

    def test_order_independence(self):
        """Result should be the same regardless of input order."""
        values1 = [80, 60, 40, 20]
        values2 = [20, 80, 40, 60]
        assert gini_coefficient(values1) == pytest.approx(gini_coefficient(values2))


class TestGiniFromStandings:
    """Tests for gini_from_standings function."""

    def test_basic_standings(self, sample_standings):
        """Should calculate Gini from standings DataFrame."""
        result = gini_from_standings(sample_standings)
        assert 0 < result < 1

    def test_equal_points(self, equal_points_standings):
        """Equal points should give Gini = 0."""
        result = gini_from_standings(equal_points_standings)
        assert result == pytest.approx(0.0)

    def test_unequal_points(self, unequal_points_standings):
        """Unequal standings should give higher Gini."""
        result = gini_from_standings(unequal_points_standings)
        assert result > 0.5

    def test_missing_column_raises(self, sample_standings):
        """Missing points column should raise ValueError."""
        with pytest.raises(ValueError, match="not found"):
            gini_from_standings(sample_standings, points_col="nonexistent")

    def test_empty_dataframe_raises(self):
        """Empty DataFrame should raise ValueError."""
        empty_df = pl.DataFrame({"points": []})
        with pytest.raises(ValueError, match="empty"):
            gini_from_standings(empty_df)

    def test_custom_points_column(self):
        """Should work with custom column name."""
        df = pl.DataFrame({"pts": [80, 70, 60, 50]})
        result = gini_from_standings(df, points_col="pts")
        assert 0 < result < 1
