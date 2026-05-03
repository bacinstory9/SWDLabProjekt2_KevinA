"""Rendert die Diagramme der Streamlit-Oberflaeche."""

import altair as alt
import pandas as pd
import streamlit as st

from timecounter.constants_and_colour import PIE_CHART_COLORS
from timecounter.core import build_weekly_share_chart_data


def render_daily_totals_chart(daily_totals: pd.DataFrame) -> None:
    """Zeigt die Tageswerte der ausgewaehlten Daten als Balkendiagramm an."""
    chart_data = daily_totals.copy()
    chart_data["day_label"] = chart_data["day_date"].dt.strftime("%d.%m.%Y")

    daily_chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("day_label:N", title="Tag", sort=chart_data["day_label"].tolist()),
            y=alt.Y("minutes:Q", title="Bildschirmzeit pro Tag"),
            tooltip=[
                alt.Tooltip("day_label:N", title="Datum"),
                alt.Tooltip("minutes:Q", title="Minuten"),
            ],
        )
    )
    st.altair_chart(daily_chart, use_container_width=True)


def render_weekly_share_chart(weekly_app_totals: pd.DataFrame) -> None:
    """Zeigt die Verteilung der Wochenminuten pro App als Kreisdiagramm an."""
    chart_data = build_weekly_share_chart_data(weekly_app_totals)
    share_chart = (
        alt.Chart(chart_data)
        .mark_arc(innerRadius=45, stroke="white", strokeWidth=2)
        .encode(
            theta=alt.Theta("weekly_app_minutes:Q", title="Minuten"),
            color=alt.Color(
                "app_name:N",
                title="App",
                scale=alt.Scale(range=PIE_CHART_COLORS),
            ),
            tooltip=[
                alt.Tooltip("app_name:N", title="App"),
                alt.Tooltip("weekly_app_minutes:Q", title="Minuten"),
                alt.Tooltip("share_label:N", title="Anzeige"),
            ],
        )
    )
    st.altair_chart(share_chart, use_container_width=True)
