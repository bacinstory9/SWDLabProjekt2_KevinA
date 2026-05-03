import pandas as pd

from timecounter.constants_and_colour import INPUT_COLUMNS


def has_required_columns(frame: pd.DataFrame) -> bool:
    return set(INPUT_COLUMNS).issubset(frame.columns)


def validate_frame(frame: pd.DataFrame, source_name: str) -> list[str]:
    issues: list[str] = []
    missing = [column for column in INPUT_COLUMNS if column not in frame.columns]
    if missing:
        return [f"{source_name}: Fehlende Spalten: {', '.join(missing)}"]

    unique_days = frame["day_date"].nunique()
    if unique_days < 3:
        issues.append(
            f"{source_name}: Es wurden nur {unique_days} Tage gefunden. Erwartet sind mindestens 3."
        )

    rank_count = frame["app_rank"].nunique()
    if rank_count > 5:
        issues.append(
            f"{source_name}: Mehr als 5 App-Ränge gefunden. Erwartet sind die Top-5 Apps."
        )

    return issues
