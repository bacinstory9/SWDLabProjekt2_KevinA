from pathlib import Path

import pandas as pd

from timecounter.data.has_required_columns import has_required_columns
from timecounter.data.parse_data import parse_data
from timecounter.data.validate_frame import validate_frame


def read_weekly_csvs(
    data_dir: Path, uploaded_files
) -> tuple[pd.DataFrame, list[str], list[str], list[str]]:
    """
Argumente:
    data_dir (Path):
        Ordner mit CSV-Dateien
    uploaded_files:
        Vom Nutzer hochgeladene Dateien

Rückgabe:
    tuple:
        - pd.DataFrame (Daten)
        - list[str] (Warnungen)
        - list[str] (geladene Dateien)
        - list[str] (Fehler)
    """

    csv_files = sorted(data_dir.glob("*.csv")) if data_dir.exists() else []
    uploaded_files = uploaded_files or []
    if not csv_files and not uploaded_files:
        return pd.DataFrame(), [], [], []

    errors: list[str] = []
    frames: list[pd.DataFrame] = []
    warnings: list[str] = []
    loaded_files: list[str] = []

    for csv_file in csv_files:
        try:
            frame = pd.read_csv(csv_file)
        except Exception as exc:
            errors.append(f"{csv_file.name}: Konnte nicht gelesen werden ({exc}).")
            continue
        issues = validate_frame(frame, csv_file.name)
        if not has_required_columns(frame):
            errors.extend(issues)
            continue
        warnings.extend(issues)
        frame["source_file"] = csv_file.name
        frames.append(frame)
        loaded_files.append(f"{csv_file.name} (Ordner)")

    for uploaded_file in uploaded_files:
        try:
            frame = pd.read_csv(uploaded_file)
        except Exception as exc:
            errors.append(f"{uploaded_file.name}: Konnte nicht gelesen werden ({exc}).")
            continue
        issues = validate_frame(frame, uploaded_file.name)
        if not has_required_columns(frame):
            errors.extend(issues)
            continue
        warnings.extend(issues)
        frame["source_file"] = uploaded_file.name
        frames.append(frame)
        loaded_files.append(f"{uploaded_file.name} (Upload)")

    if not frames:
        return pd.DataFrame(), warnings, loaded_files, errors

    data = parse_data(frames)
    return data, warnings, loaded_files, errors
