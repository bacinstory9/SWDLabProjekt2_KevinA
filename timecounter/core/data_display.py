"""Bereitet Kennzahlen und Tabellen für die Darstellung in der App auf."""

import pandas as pd


def format_minutes(minutes: float) -> str:
    """Formatiert Minuten als lesbaren String im Format 'X h YY min'."""
    total_minutes = int(round(minutes))
    hours, mins = divmod(total_minutes, 60)
    return f"{hours} h {mins:02d} min"


def build_daily_totals(data: pd.DataFrame) -> pd.DataFrame:
    """Verdichtet die Daten auf einen Tageswert pro Datum."""
    return (
        data.drop_duplicates(subset=["week_start", "day_date"])
        .loc[
            :,
            ["week_start", "week_label", "day_date", "day_name", "daily_total_minutes"],
        ]
        .sort_values(["week_start", "day_date"])
        .rename(columns={"daily_total_minutes": "minutes"})
    )


def build_weekly_totals(data: pd.DataFrame) -> pd.DataFrame:
    """Verdichtet die Daten auf einen Gesamtwert pro Woche."""
    return (
        data.groupby(["week_start", "week_label"], as_index=False)[
            "weekly_total_minutes"
        ]
        .max()
        .sort_values("week_start")
        .rename(columns={"weekly_total_minutes": "minutes"})
    )


def build_weekly_app_totals(data: pd.DataFrame) -> pd.DataFrame:
    """Berechnet die Wochenminuten je App für jede Woche."""
    return (
        data.groupby(["week_start", "week_label", "app_name"], as_index=False)[
            "weekly_app_minutes"
        ]
        .max()
        .sort_values(["week_start", "weekly_app_minutes"], ascending=[True, False])
    )


def build_weekly_share_chart_data(weekly_app_totals: pd.DataFrame) -> pd.DataFrame:
    """Schreibt App-Wochenwerte um ein formatiertes Label für das Kreisdiagramm."""
    chart_data = weekly_app_totals.loc[:, ["app_name", "weekly_app_minutes"]].copy()
    chart_data["share_label"] = chart_data["weekly_app_minutes"].map(format_minutes)
    return chart_data


def build_stats_table(weekly_totals: pd.DataFrame) -> pd.DataFrame:
    """Erzeugt eine kompakte Statistik-Tabelle aus den Wochenwerten."""
    stats = {
        "Kennzahl": [
            "Anzahl erfasster Wochen",
            "Durchschnitt pro Woche",
            "Median pro Woche",
            "Maximum pro Woche",
            "Minimum pro Woche",
        ],
        "Wert": [
            str(len(weekly_totals)),
            format_minutes(weekly_totals["minutes"].mean()),
            format_minutes(weekly_totals["minutes"].median()),
            format_minutes(weekly_totals["minutes"].max()),
            format_minutes(weekly_totals["minutes"].min()),
        ],
    }
    return pd.DataFrame(stats)
