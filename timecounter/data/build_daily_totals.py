import pandas as pd


def build_daily_totals(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.drop_duplicates(subset=["week_start", "day_date"])
        .loc[:, ["week_start", "week_label", "day_date", "day_name", "daily_total_minutes"]]
        .sort_values(["week_start", "day_date"])
        .rename(columns={"daily_total_minutes": "minutes"})
    )
