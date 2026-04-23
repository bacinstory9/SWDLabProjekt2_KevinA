import pandas as pd

from timecounter.constants import INPUT_COLUMNS


def has_required_columns(frame: pd.DataFrame) -> bool:
    return set(INPUT_COLUMNS).issubset(frame.columns)
