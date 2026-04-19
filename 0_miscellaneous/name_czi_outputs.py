from __future__ import annotations

from pathlib import Path

import pandas as pd


CZI_FOLDER = Path(r"C:\Users\Ingvild\Downloads\d-9a20cefe-16d4-4c80-b238-9c3d8e2260d1-Mouse11-1_CZI")
SUBJECT_ID = "mouse11"
AGE = "P120"
SEX = "M"
OUTPUT_PATH = CZI_FOLDER / f"{SUBJECT_ID}_{AGE}_{SEX}_preprocessing.xlsx"


EXPECTED_COLUMNS = [
    "Input file name",
    "Renamed",
    "Rotation CCW",
    "Scale X",
    "Scale Y",
    "Photoshop adjustments",
]


def split_czi_stem(stem: str) -> tuple[str, list[str]]:
    parts = stem.split("_")
    section_numbers: list[str] = []

    while parts and parts[-1] == "Control":
        parts.pop()

    while parts and parts[-1].isdigit() and len(parts[-1]) == 3:
        section_numbers.append(parts.pop())

    section_numbers.reverse()

    if not parts or not section_numbers:
        raise ValueError(
            "Expected CZI names like 'mouse883_P21_F_parv_005_011_017.czi', "
            f"but got '{stem}.czi'."
        )

    return "_".join(parts), section_numbers


def build_manifest_rows(czi_folder: Path, subject_id: str, age: str, sex: str) -> list[dict[str, str | int]]:
    czi_paths = sorted(czi_folder.glob("*.czi"))
    if not czi_paths:
        raise FileNotFoundError(f"No .czi files found in {czi_folder}")

    rows: list[dict[str, str | int]] = []

    for czi_path in czi_paths:
        prefix, section_numbers = split_czi_stem(czi_path.stem)
        prefix_parts = prefix.split("_")

        if len(prefix_parts) < 4:
            raise ValueError(
                f"Expected at least subject, age, sex, and stain in '{czi_path.name}', "
                f"but found '{prefix}'."
            )

        stain = "_".join(prefix_parts[3:])

        for scene_index, section_number in enumerate(section_numbers, start=1):
            rows.append(
                {
                    "Input file name": f"{czi_path.stem}_s{scene_index}",
                    "Renamed": f"{subject_id}_{age}_{sex}_{stain}_s{section_number}",
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
    rows = build_manifest_rows(
        czi_folder=CZI_FOLDER,
        subject_id=SUBJECT_ID,
        age=AGE,
        sex=SEX,
    )
    save_manifest(rows=rows, output_path=OUTPUT_PATH)
    print(f"Saved {len(rows)} expected TIFF exports to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
