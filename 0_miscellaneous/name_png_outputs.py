from __future__ import annotations

from pathlib import Path

import pandas as pd


PNG_FOLDER = Path(r"D:\CalciMAP\P120\Parvalbumin\Mouse81267\thumbnails")
SUBJECT_ID = "mouse81267"
AGE = "P120"
SEX = "M"
OUTPUT_PATH = PNG_FOLDER / f"{SUBJECT_ID}_{AGE}_{SEX}_preprocessing.xlsx"


EXPECTED_COLUMNS = [
    "Input file name",
    "Renamed",
    "Rotation CCW",
    "Scale X",
    "Scale Y",
    "Photoshop adjustments",
]


def build_manifest_rows(png_folder: Path) -> list[dict[str, str | int]]:
    png_paths = sorted(png_folder.glob("*.png"))
    if not png_paths:
        raise FileNotFoundError(f"No .png files found in {png_folder}")

    rows: list[dict[str, str | int]] = []
    for png_path in png_paths:
        rows.append(
            {
                "Input file name": "",
                "Renamed": png_path.stem,
                "Rotation CCW": 0,
                "Scale X": 1,
                "Scale Y": 1,
                "Photoshop adjustments": "",
            }
        )

    return rows


def save_manifest(rows: list[dict[str, str | int]], output_path: Path) -> None:
    manifest_df = pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        manifest_df.to_excel(output_path, index=False)
    except ModuleNotFoundError as exc:
        if exc.name == "openpyxl":
            raise ModuleNotFoundError(
                "Saving .xlsx files requires openpyxl. Install it with 'pip install openpyxl' "
                "and run the script again."
            ) from exc
        raise


def main() -> None:
    rows = build_manifest_rows(png_folder=PNG_FOLDER)
    save_manifest(rows=rows, output_path=OUTPUT_PATH)
    print(f"Saved {len(rows)} PNG entries to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
