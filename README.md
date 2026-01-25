# Football League Competitiveness Analysis

Analyze Portuguese Primeira Liga competitiveness over 10 years using Gini coefficients and point gap metrics.

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras
```

## Usage

### Interactive Notebook

```bash
uv run marimo edit notebooks/exploration.py
```

When prompted, choose "Don't use sandbox" to reuse the project virtualenv.

Opens a reactive notebook with:
- Season selector for filtering data
- Gini coefficient trend chart
- Point gaps visualization (1st-2nd, 1st-4th, 1st-last)
- Summary statistics

### As a Library

```python
from football_competitiveness.data import StandingsFetcher
from football_competitiveness.metrics import gini_from_standings, calculate_point_gaps

fetcher = StandingsFetcher()
standings = fetcher.fetch_standings("2023-2024")

# Calculate metrics
gini = gini_from_standings(standings)
gaps = calculate_point_gaps(standings)

print(f"Gini coefficient: {gini:.3f}")
print(f"Title race gap: {gaps.first_second} points")
print(f"UCL spots gap: {gaps.first_fourth} points")
```

## Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| Gini Coefficient | Inequality in final points distribution | 0 = equal, 1 = max inequality |
| 1st-2nd Gap | Points between champion and runner-up | Title race competitiveness |
| 1st-4th Gap | Points between champion and 4th place | Champions League qualification battle |
| 1st-Last Gap | Points between champion and bottom team | Overall league spread |

## Project Structure

```
football/
├── src/football_competitiveness/
│   ├── config.py           # League and analysis configuration
│   ├── data/fetcher.py     # Standings data loader
│   ├── metrics/
│   │   ├── gini.py         # Gini coefficient calculation
│   │   └── point_gaps.py   # Point gap metrics
│   └── visualization/
│       └── charts.py       # Altair chart functions
├── data/
│   └── primeira_liga_standings.csv  # Historical standings (2014-2024)
├── notebooks/
│   └── exploration.py      # Marimo interactive notebook
└── tests/                  # Unit tests
```

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=football_competitiveness

# Lint
uv run ruff check src/
```

## Data

Historical standings for Portuguese Primeira Liga bundled in `data/primeira_liga_standings.csv`.

**Seasons:** 2014-15 through 2023-24 (10 seasons, 18 teams each)

Source: [FBref](https://fbref.com/)
