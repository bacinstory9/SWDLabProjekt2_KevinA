import pandas as pd

from timecounter.constants import CALCULATED_COLUMNS


def add_calculated_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """
Argumente:
    frame (pd.DataFrame):
        Rohdaten

Rückgabe:
    pd.DataFrame:
        Daten mit berechneten Spalten:
        - weekly_app_minutes
        - weekly_total_minutes
    """

    data = frame.copy()
    data["day_date"] = pd.to_datetime(data["day_date"], errors="coerce")
    data["daily_total_minutes"] = pd.to_numeric(data["daily_total_minutes"], errors="coerce")
    data["daily_app_minutes"] = pd.to_numeric(data["daily_app_minutes"], errors="coerce")
    data["week_start"] = data["day_date"] - pd.to_timedelta(data["day_date"].dt.weekday, unit="D")

    weekly_totals = (
        data.drop_duplicates(subset=["week_label", "week_start", "day_date"])
        .groupby(["week_label", "week_start"])["daily_total_minutes"]
        .sum(min_count=1)
        .rename("weekly_total_minutes")
        .reset_index()
    )
    weekly_app_totals = (
        data.groupby(["week_label", "week_start", "app_name"])["daily_app_minutes"]
        .sum(min_count=1)
        .rename("weekly_app_minutes")
        .reset_index()
    )

    data = data.drop(columns=CALCULATED_COLUMNS, errors="ignore")
    data = data.merge(weekly_totals, on=["week_label", "week_start"], how="left")
    data = data.merge(weekly_app_totals, on=["week_label", "week_start", "app_name"], how="left")
    return data.drop(columns=["week_start"])
