import pandas as pd


def filter_by_week_labels(data: pd.DataFrame, week_labels: list[str]) -> pd.DataFrame:
    return data[data["week_label"].isin(week_labels)]
