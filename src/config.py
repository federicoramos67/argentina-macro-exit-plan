from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

START_YEAR = 1990
END_YEAR = 2024

# (start_year, end_year, label, color)
GOVERNMENTS: list[tuple[int, int, str, str]] = [
    (1990, 1999, "Menem", "lightblue"),
    (1999, 2001, "De la Rúa", "lightgreen"),
    (2002, 2003, "Duhalde", "khaki"),
    (2003, 2007, "N. Kirchner", "orange"),
    (2007, 2015, "C. Kirchner", "salmon"),
    (2015, 2019, "Macri", "lightgrey"),
    (2019, 2023, "A. Fernández", "plum"),
    (2023, 2025, "Milei", "lightyellow"),
]

MAX_INFLATION_PCT = 5000.0
MIN_UNEMPLOYMENT_PCT = 0.0
MIN_POVERTY_PCT = 0.0
