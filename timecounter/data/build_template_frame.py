import pandas as pd

from timecounter.constants import INPUT_COLUMNS


def build_template_frame() -> pd.DataFrame:
    """
Argumente:
    Keine

Rückgabe:
    pd.DataFrame:
        Beispiel-Datensatz mit Bildschirmzeit-Daten;
        nur am Anfang vor dem Hochladen des echten Datensatz angezeigt werden (Platzspeicher)
    """

    rows = [
        ["2026-W15", "2026-04-07", "Dienstag", 210, 1, "YouTube", 50],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 2, "WhatsApp", 40],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 3, "Safari", 35],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 4, "Moodle", 28],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 5, "Spotify", 20],
        ["2026-W15", "2026-04-09", "Donnerstag", 245, 1, "YouTube", 62],
        ["2026-W15", "2026-04-09", "Donnerstag", 245, 2, "WhatsApp", 45],
        ["2026-W15", "2026-04-09", "Donnerstag", 245, 3, "Safari", 40],
        ["2026-W15", "2026-04-09", "Donnerstag", 245, 4, "Moodle", 30],
        ["2026-W15", "2026-04-09", "Donnerstag", 245, 5, "Spotify", 24],
        ["2026-W15", "2026-04-11", "Samstag", 225, 1, "YouTube", 68],
        ["2026-W15", "2026-04-11", "Samstag", 225, 2, "WhatsApp", 43],
        ["2026-W15", "2026-04-11", "Samstag", 225, 3, "Safari", 37],
        ["2026-W15", "2026-04-11", "Samstag", 225, 4, "Moodle", 31],
        ["2026-W15", "2026-04-11", "Samstag", 225, 5, "Spotify", 19],
    ]
    return pd.DataFrame(rows, columns=INPUT_COLUMNS)
