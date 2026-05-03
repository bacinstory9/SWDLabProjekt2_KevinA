import pandas as pd


def build_week_selector_options(data: pd.DataFrame) -> list[str]:
    week_index = (
        data.loc[:, ["week_start", "week_label"]]
        .drop_duplicates()
        .sort_values("week_start")
    )
    return week_index["week_label"].tolist()


def filter_by_week_labels(data: pd.DataFrame, week_labels: list[str]) -> pd.DataFrame:
    return data[data["week_label"].isin(week_labels)]
