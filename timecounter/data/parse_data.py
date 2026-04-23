import pandas as pd

from timecounter.data.add_calculated_columns import add_calculated_columns


def parse_data(frames: list[pd.DataFrame]) -> pd.DataFrame:
    """
Argumente:
    frames (list[pd.DataFrame]):
        Liste von DataFrames

Rückgabe:
    pd.DataFrame:
        Zusammengeführte und bereinigte Daten
    """

    data = pd.concat([add_calculated_columns(frame) for frame in frames], ignore_index=True)
    data["day_date"] = pd.to_datetime(data["day_date"], errors="coerce")
    data["week_start"] = data["day_date"] - pd.to_timedelta(data["day_date"].dt.weekday, unit="D")
    for column in [
        "daily_total_minutes",
        "app_rank",
        "daily_app_minutes",
        "weekly_app_minutes",
        "weekly_total_minutes",
    ]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data
