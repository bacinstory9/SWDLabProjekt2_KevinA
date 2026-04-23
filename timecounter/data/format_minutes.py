def format_minutes(minutes: float) -> str:
    """
Argumente:
    minutes (float):
        Zeit in Minuten

Rückgabe:
    str:
        Formatierte Zeit als "X h YY min"
        -> mit divmod (*Anzahl der Minuten, 60) (durch 60 geteilt werden)
    """

    total_minutes = int(round(minutes))
    hours, mins = divmod(total_minutes, 60)
    return f"{hours} h {mins:02d} min"
