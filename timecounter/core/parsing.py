from pathlib import Path

import pandas as pd

from timecounter.constants_and_colour import CALCULATED_COLUMNS, INPUT_COLUMNS
from timecounter.core.error_handling import has_required_columns, validate_frame


def add_calculated_columns(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    data["day_date"] = pd.to_datetime(data["day_date"], errors="coerce")
    data["daily_total_minutes"] = pd.to_numeric(
        data["daily_total_minutes"], errors="coerce"
    )
    data["daily_app_minutes"] = pd.to_numeric(
        data["daily_app_minutes"], errors="coerce"
    )
    data["week_start"] = data["day_date"] - pd.to_timedelta(
        data["day_date"].dt.weekday, unit="D"
    )

    weekly_totals = (
        data.drop_duplicates(subset=["week_label", "week_start", "day_date"])
        .groupby(["week_label", "week_start"])["daily_total_minutes"]
        .sum(min_count=1)
        .rename("weekly_total_minutes")
        .reset_index()
    )
    weekly_app_totals = (
        data.groupby(["week_label", "week_start", "app_name"])["daily_app_minutes"]
        .sum(min_count=1)
        .rename("weekly_app_minutes")
        .reset_index()
    )

    data = data.drop(columns=CALCULATED_COLUMNS, errors="ignore")
    data = data.merge(weekly_totals, on=["week_label", "week_start"], how="left")
    data = data.merge(
        weekly_app_totals, on=["week_label", "week_start", "app_name"], how="left"
    )
    return data.drop(columns=["week_start"])


def build_template_frame() -> pd.DataFrame:
    rows = [
        ["2026-W15", "2026-04-07", "Dienstag", 210, 1, "YouTube", 50],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 2, "WhatsApp", 40],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 3, "Safari", 35],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 4, "Moodle", 28],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 5, "Spotify", 20],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 1, "YouTube", 50],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 2, "WhatsApp", 40],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 3, "Safari", 35],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 4, "Moodle", 28],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 5, "Spotify", 20],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 1, "YouTube", 50],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 2, "WhatsApp", 40],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 3, "Safari", 35],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 4, "Moodle", 28],
        ["2026-W15", "2026-04-07", "Dienstag", 210, 5, "Spotify", 20],
    ]
    return pd.DataFrame(rows, columns=INPUT_COLUMNS)


def parse_data(frames: list[pd.DataFrame]) -> pd.DataFrame:
    data = pd.concat(
        [add_calculated_columns(frame) for frame in frames], ignore_index=True
    )
    data["day_date"] = pd.to_datetime(data["day_date"], errors="coerce")
    data["week_start"] = data["day_date"] - pd.to_timedelta(
        data["day_date"].dt.weekday, unit="D"
    )

    numeric_columns = [
        "daily_total_minutes",
        "app_rank",
        "daily_app_minutes",
        "weekly_app_minutes",
        "weekly_total_minutes",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


def read_weekly_csvs(
    data_dir: Path, uploaded_files
) -> tuple[pd.DataFrame, list[str], list[str], list[str]]:
    csv_files = sorted(data_dir.glob("*.csv")) if data_dir.exists() else []
    uploaded_files = uploaded_files or []
    if not csv_files and not uploaded_files:
        return pd.DataFrame(), [], [], []

    errors: list[str] = []
    warnings: list[str] = []
    loaded_files: list[str] = []
    frames: list[pd.DataFrame] = []

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

    return parse_data(frames), warnings, loaded_files, errors
