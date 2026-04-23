import pandas as pd

from timecounter.data.format_minutes import format_minutes


def build_stats_table(weekly_totals: pd.DataFrame) -> pd.DataFrame:
    stats = {
        "Kennzahl": [
            "Anzahl erfasster Wochen",
            "Durchschnitt pro Woche",
            "Median pro Woche",
            "Maximum pro Woche",
            "Minimum pro Woche",
        ],
        "Wert": [
            str(len(weekly_totals)),
            format_minutes(weekly_totals["minutes"].mean()),
            format_minutes(weekly_totals["minutes"].median()),
            format_minutes(weekly_totals["minutes"].max()),
            format_minutes(weekly_totals["minutes"].min()),
        ],
    }
    return pd.DataFrame(stats)
