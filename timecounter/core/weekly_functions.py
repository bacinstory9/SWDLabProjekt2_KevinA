"""Hilfsfunktionen für Wochenauswahl und Filterlogik."""

import pandas as pd


def build_week_selector_options(data: pd.DataFrame) -> list[str]:
    """Erzeugen sortierte Auswahlwerte für den Wochenfilter in der Sidebar."""
    week_index = (
        data.loc[:, ["week_start", "week_label"]]
        .drop_duplicates()
        .sort_values("week_start")
    )
    return week_index["week_label"].tolist()


def filter_by_week_labels(data: pd.DataFrame, week_labels: list[str]) -> pd.DataFrame:
    """Filter die Daten auf die ausgewählten Wochenlabels, schreib das enstsprechende Datum für jede."""
    return data[data["week_label"].isin(week_labels)]
