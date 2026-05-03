"""Sammelt die Kernfunktionen für Parsing, Validierung (Error Handling) und Diagrammendarstelung (Daten Display)."""

from .parsing import build_template_frame, parse_data, read_weekly_csvs
from .data_display import (
    build_daily_totals,
    build_stats_table,
    build_weekly_app_totals,
    build_weekly_share_chart_data,
    build_weekly_totals,
    format_minutes,
)
from .error_handling import has_required_columns, validate_frame
from .weekly_functions import build_week_selector_options, filter_by_week_labels

__all__ = [
    "build_daily_totals",
    "build_stats_table",
    "build_template_frame",
    "build_week_selector_options",
    "build_weekly_app_totals",
    "build_weekly_share_chart_data",
    "build_weekly_totals",
    "filter_by_week_labels",
    "format_minutes",
    "has_required_columns",
    "parse_data",
    "read_weekly_csvs",
    "validate_frame",
]
