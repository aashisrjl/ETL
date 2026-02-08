"""Generate grounds.xlsx from grounds.csv

Usage:
    pip install pandas openpyxl
    python data/raw/generate_grounds_xlsx.py

This writes data/raw/grounds.xlsx with sheet name 'grounds'.
"""
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent / "grounds.csv"
XLSX_PATH = Path(__file__).parent / "grounds.xlsx"

if not CSV_PATH.exists():
    print(f"CSV not found: {CSV_PATH}")
    raise SystemExit(1)

df = pd.read_csv(CSV_PATH)

df.to_excel(XLSX_PATH, sheet_name="grounds", index=False)
print(f"Wrote {XLSX_PATH}")
