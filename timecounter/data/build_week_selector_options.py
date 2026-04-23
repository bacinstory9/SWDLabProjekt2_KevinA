import pandas as pd


def build_week_selector_options(data: pd.DataFrame) -> list[str]:
    """
    ~_~
    """

    week_index = data.loc[:, ["week_start", "week_label"]].drop_duplicates().sort_values("week_start")
    return week_index["week_label"].tolist()
