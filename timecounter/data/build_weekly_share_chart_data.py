import pandas as pd

from timecounter.data.format_minutes import format_minutes


def build_weekly_share_chart_data(weekly_app_totals: pd.DataFrame) -> pd.DataFrame:
    """
Argumente:
    weekly_app_totals (pd.DataFrame):
        Wöchentliche App-Nutzung

Rückgabe:
    None:
        Zeigt ein Kreisdiagramm in Streamlit
    """

    chart_data = weekly_app_totals.loc[:, ["app_name", "weekly_app_minutes"]].copy()
    chart_data["share_label"] = chart_data["weekly_app_minutes"].map(format_minutes)
    return chart_data
