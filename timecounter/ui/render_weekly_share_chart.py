import altair as alt
import pandas as pd
import streamlit as st

from timecounter.constants import PIE_CHART_COLORS
from timecounter.data.build_weekly_share_chart_data import build_weekly_share_chart_data


def render_weekly_share_chart(weekly_app_totals: pd.DataFrame) -> None:
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
