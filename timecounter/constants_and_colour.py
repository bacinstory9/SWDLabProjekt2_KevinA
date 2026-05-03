"""Zentrale Konstanten für Dateipfade, Spaltennamen und Diagrammfarben."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "TimeCounterData"
PIE_CHART_COLORS = ["#005F73", "#EE6C4D", "#FFB703", "#2A9D8F", "#9B2226"]
INPUT_COLUMNS = [
    "week_label",
    "day_date",
    "day_name",
    "daily_total_minutes",
    "app_rank",
    "app_name",
    "daily_app_minutes",
]
CALCULATED_COLUMNS = [
    "weekly_app_minutes",
    "weekly_total_minutes",
]
REQUIRED_COLUMNS = INPUT_COLUMNS + CALCULATED_COLUMNS
