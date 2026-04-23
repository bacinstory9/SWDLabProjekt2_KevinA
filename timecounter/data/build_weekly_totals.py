import pandas as pd


def build_weekly_totals(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby(["week_start", "week_label"], as_index=False)["weekly_total_minutes"]
        .max()
        .sort_values("week_start")
        .rename(columns={"weekly_total_minutes": "minutes"})
    )
