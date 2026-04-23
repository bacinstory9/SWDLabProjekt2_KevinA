import pandas as pd


def build_weekly_app_totals(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby(["week_start", "week_label", "app_name"], as_index=False)["weekly_app_minutes"]
        .max()
        .sort_values(["week_start", "weekly_app_minutes"], ascending=[True, False])
    )
