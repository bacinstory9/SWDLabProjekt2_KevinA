"""Rendert alternative UI-Zustaende wie den leeren Start ohne Nutzerdaten."""

import pandas as pd
import streamlit as st

from timecounter.core import build_template_frame, parse_data


def render_empty_state() -> pd.DataFrame:
    """Zeigt Beispiel- und Hilfsdaten an, wenn noch keine CSV-Dateien geladen wurden."""
    template_frame = build_template_frame()
    st.warning(
        "Noch keine CSV-Dateien geladen. Die App zeigt deshalb zunächst die schon eingebauten Beispieldaten an."
    )
    st.subheader("So können Sie Ihre eigenen CSV-Dateien erstellen :")
    st.markdown(
        """
1. Erstellen Sie eine eigene CSV-Datei.
2. Erfassen Sie mindestens drei verschiedene Tage dieser Woche.
3. Schreiben Sie pro Tag genau fünf Zeilen, eine pro Top-App.
4. Verwenden Sie Minuten als Zahlen ohne Einheiten.
** `weekly_app_minutes` und `weekly_total_minutes` werden automatisch berechnet.
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
