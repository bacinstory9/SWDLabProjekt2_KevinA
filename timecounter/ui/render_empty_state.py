import pandas as pd
import streamlit as st

from timecounter.data.build_template_frame import build_template_frame
from timecounter.data.parse_data import parse_data


def render_empty_state() -> pd.DataFrame:
    template_frame = build_template_frame()
    st.warning(
        "Noch keine CSV-Dateien geladen. Die App zeigt deshalb zunaechst die eingebauten Beispieldaten an."
    )
    st.subheader("So erstellen Sie Ihre eigenen CSV-Dateien")
    st.markdown(
        """
1. Erstellen Sie pro Woche eine eigene CSV-Datei.
2. Erfassen Sie mindestens drei verschiedene Tage dieser Woche.
3. Schreiben Sie pro Tag genau fuenf Zeilen, eine pro Top-App.
4. Verwenden Sie Minuten als Zahlen ohne Einheiten.
5. `weekly_app_minutes` und `weekly_total_minutes` werden automatisch berechnet.
        """
    )
    st.subheader("Tabellenvorlage")
    st.dataframe(template_frame, hide_index=True, use_container_width=True)
    st.download_button(
        "CSV-Vorlage herunterladen",
        data=template_frame.to_csv(index=False).encode("utf-8"),
        file_name="TimeCounterTemplate.csv",
        mime="text/csv",
    )
    return parse_data([template_frame])
