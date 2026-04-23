import altair as alt
import pandas as pd
import streamlit as st


def render_daily_totals_chart(daily_totals: pd.DataFrame) -> None:
    """
Argumente:
    daily_totals (pd.DataFrame):
        Tagesdaten

Rückgabe:
    None:
        Zeigt ein Balkendiagramm in Streamlit
    """

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
