"""Startet die Streamlit-Oberfläche (UI) für die Bildschirmzeit-Analyse."""

import sys
from pathlib import Path

import streamlit as st

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from timecounter.constants_and_colour import DATA_DIR
from timecounter.core import (
    build_daily_totals,
    build_stats_table,
    build_week_selector_options,
    build_weekly_app_totals,
    build_weekly_totals,
    filter_by_week_labels,
    format_minutes,
    read_weekly_csvs,
)
from timecounter.ui import (
    render_daily_totals_chart,
    render_empty_state,
    render_weekly_share_chart,
)


def main() -> None:
    """Baut die App-Oberfläche (UI) auf und verbindet die Datenquelle mit Auswertungen/Analysen."""
    st.set_page_config(
        page_title="Bildschirmzeit im Semester",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.title("Bildschirmzeit im Semester")
    st.caption("Kevin Alessander - DS")
    st.caption(
        "Visualisierung der wöchentlichen Bildschirmzeit inklusive Tageswerten und Top-5-Apps."
    )

    with st.sidebar:
        st.header("Datenquelle")
        uploaded_files = st.file_uploader(
            "CSV-Dateien hochladen",
            type="csv",
            accept_multiple_files=True,
            help="Sie können eine oder mehrere Wochen-Dateien direkt hochladen.",
        )

    data, warnings, loaded_files, errors = read_weekly_csvs(DATA_DIR, uploaded_files)

    for error in errors:
        st.error(error)

    if data.empty:
        data = render_empty_state()
        loaded_files = ["Eingebautes Beispiel"]

    for warning in warnings:
        st.warning(warning)

    data = data.dropna(subset=["day_date", "week_start"])
    if data.empty:
        st.error(
            "Die geladenen Dateien enthalten keine gueltigen Datumswerte für 'day_date'."
        )
        render_empty_state()
        st.stop()

    available_week_labels = build_week_selector_options(data)

    with st.sidebar:
        st.header("Steuerung")
        selected_week_labels = st.multiselect(
            "Wochen anzeigen",
            options=available_week_labels,
            default=available_week_labels,
            help="Wählen Sie die Wochen aus, die in allen Diagrammen angezeigt werden sollen.",
        )
        available_apps = sorted(data["app_name"].dropna().unique().tolist())
        selected_apps = st.multiselect(
            "Apps für den Verlauf",
            options=available_apps,
            default=available_apps,
        )
        st.markdown("**Geladene Dateien**")
        for file_name in loaded_files:
            st.write(file_name)

    if not selected_week_labels:
        st.info("Wählen Sie in der Sidebar mindestens eine Woche aus.")
        st.stop()

    filtered_data = filter_by_week_labels(data, selected_week_labels)

    if filtered_data.empty:
        st.info("Für die ausgewählten Wochen sind keine Daten vorhanden.")
        st.stop()

    weekly_totals = build_weekly_totals(filtered_data)
    daily_totals = build_daily_totals(filtered_data)
    weekly_app_totals = build_weekly_app_totals(filtered_data)
    stats_table = build_stats_table(weekly_totals)

    metric_columns = st.columns(4)
    metric_columns[0].metric("Wochen gesamt", str(len(weekly_totals)))
    metric_columns[1].metric(
        "Durchschnitt / Woche", format_minutes(weekly_totals["minutes"].mean())
    )
    metric_columns[2].metric(
        "Maximale Woche", format_minutes(weekly_totals["minutes"].max())
    )
    metric_columns[3].metric(
        "Durchschnitt / Tag", format_minutes(daily_totals["minutes"].mean())
    )

    left_col, right_col = st.columns([1.7, 1])

    with left_col:
        st.subheader("Zeitlicher Verlauf gesamt")
        st.line_chart(
            weekly_totals.set_index("week_start")
            .loc[:, ["minutes"]]
            .rename(columns={"minutes": "Bildschirmzeit pro Woche"})
        )

    with right_col:
        st.subheader("Statistische Kennzahlen")
        st.dataframe(stats_table, hide_index=True, use_container_width=True)

    st.subheader("Verlauf nach App")
    if selected_apps:
        st.line_chart(
            weekly_app_totals[weekly_app_totals["app_name"].isin(selected_apps)]
            .pivot(index="week_start", columns="app_name", values="weekly_app_minutes")
            .sort_index()
        )
    else:
        st.info("Wählen Sie in der Sidebar mindestens eine App aus.")

    week_options = weekly_totals.sort_values("week_start")["week_label"].tolist()
    selected_week_label = st.select_slider(
        "Detailansicht für eine Woche",
        options=week_options,
        value=week_options[-1],
    )

    selected_week_data = filtered_data[
        filtered_data["week_label"] == selected_week_label
    ]
    selected_week_daily = build_daily_totals(selected_week_data)
    selected_week_apps = build_weekly_app_totals(selected_week_data)
    detail_col_1, detail_col_2 = st.columns(2)

    with detail_col_1:
        st.subheader("Tageswerte der ausgewählten Woche")
        render_daily_totals_chart(selected_week_daily)

    with detail_col_2:
        st.subheader("Top-5-Apps der ausgewählten Woche")
        render_weekly_share_chart(selected_week_apps)
        st.dataframe(
            selected_week_apps.loc[:, ["app_name", "weekly_app_minutes"]].rename(
                columns={
                    "app_name": "App",
                    "weekly_app_minutes": "Minuten in der Woche",
                }
            ),
            hide_index=True,
            use_container_width=True,
        )

    st.subheader("Rohdaten")
    st.dataframe(
        filtered_data.drop(columns=["week_start"], errors="ignore").sort_values(
            ["day_date", "app_rank"]
        ),
        hide_index=True,
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
