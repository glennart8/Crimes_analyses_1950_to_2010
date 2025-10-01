from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # två nivåer till rooten
CSV_PATH = BASE_DIR / "backend" / "data" / "cleaned_data.csv"
