"""Gini coefficient calculation for measuring points inequality."""

import numpy as np
import polars as pl


def gini_coefficient(values: np.ndarray | pl.Series | list[int | float]) -> float:
    """Calculate the Gini coefficient for a distribution of values.

    The Gini coefficient measures inequality in a distribution:
    - 0 = perfect equality (all teams have same points)
    - 1 = maximum inequality (one team has all points)

    Uses the formula: G = (2 * Σ(i * x_i)) / (n * Σx_i) - (n + 1) / n
    where x_i are sorted values and i is the 1-based rank.

    Args:
        values: Array-like of non-negative values (e.g., points)

    Returns:
        Gini coefficient between 0 and 1

    Raises:
        ValueError: If values is empty or contains negative values
    """
    # Convert to numpy array
    if isinstance(values, pl.Series):
        arr = values.to_numpy()
    elif isinstance(values, list):
        arr = np.array(values)
    else:
        arr = np.asarray(values)

    # Validate input
    if len(arr) == 0:
        raise ValueError("Cannot calculate Gini coefficient for empty array")

    if np.any(arr < 0):
        raise ValueError("Gini coefficient requires non-negative values")

    # Handle edge case: all zeros
    if np.sum(arr) == 0:
        return 0.0

    # Sort values
    sorted_arr = np.sort(arr)
    n = len(sorted_arr)

    # Calculate Gini using the formula
    # G = (2 * Σ(i * x_i)) / (n * Σx_i) - (n + 1) / n
    indices = np.arange(1, n + 1)
    gini = (2 * np.sum(indices * sorted_arr)) / (n * np.sum(sorted_arr)) - (n + 1) / n

    return float(gini)


def gini_from_standings(standings: pl.DataFrame, points_col: str = "points") -> float:
    """Calculate Gini coefficient from a standings DataFrame.

    Args:
        standings: DataFrame containing team standings
        points_col: Name of the column containing points

    Returns:
        Gini coefficient between 0 and 1

    Raises:
        ValueError: If points column doesn't exist or standings is empty
    """
    if points_col not in standings.columns:
        raise ValueError(f"Column '{points_col}' not found in standings")

    if standings.is_empty():
        raise ValueError("Standings DataFrame is empty")

    points = standings[points_col]
    return gini_coefficient(points)
