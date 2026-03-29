from __future__ import annotations

from pathlib import Path

import pandas as pd


METADATA_XLSX_PATH = Path(r"D:\CalciMAP\investigator_analysis\Animal metadata.xlsx")
SHEET_NAME = "Processing_progress"
OUTPUT_PATH = Path(__file__).resolve().parent / "technical_variability_analysis" / "immunostaining_metadata.csv"
TARGET_MARKERS = ["calbindin", "parvalbumin"]


metadata_df = pd.read_excel(METADATA_XLSX_PATH, sheet_name=SHEET_NAME, header=1)
metadata_df.columns = metadata_df.columns.str.strip()
metadata_df["ID"] = metadata_df["ID"].ffill()
metadata_df["Marker"] = metadata_df["Marker"].ffill()
metadata_df["immunostaining by"] = metadata_df["immunostaining by"].ffill()

metadata_df["ID"] = pd.to_numeric(metadata_df["ID"], errors="coerce")
metadata_df["Marker"] = metadata_df["Marker"].astype(str).str.strip().str.lower()
metadata_df["immunostaining by"] = metadata_df["immunostaining by"].astype(str).str.strip()

metadata_df = metadata_df.loc[
    metadata_df["ID"].notna()
    & metadata_df["Marker"].isin(TARGET_MARKERS)
    & metadata_df["immunostaining by"].ne("")
    & metadata_df["immunostaining by"].ne("nan"),
    ["ID", "Marker", "immunostaining by"],
].copy()

metadata_df["subject_number"] = metadata_df["ID"].astype(int).astype(str)
metadata_df = metadata_df.rename(
    columns={
        "Marker": "stain",
        "immunostaining by": "immunostaining_by",
    }
)
metadata_df = metadata_df[["subject_number", "stain", "immunostaining_by"]].drop_duplicates()

investigator_order = sorted(metadata_df["immunostaining_by"].dropna().unique())
investigator_map = {
    investigator_name: f"Investigator {index + 1}"
    for index, investigator_name in enumerate(investigator_order)
}
metadata_df["immunostaining_by"] = metadata_df["immunostaining_by"].map(investigator_map)

metadata_df = metadata_df.sort_values(["stain", "subject_number"]).reset_index(drop=True)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
metadata_df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved immunostaining metadata to: {OUTPUT_PATH}")
