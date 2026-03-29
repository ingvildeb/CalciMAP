from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(r"D:\CalciMAP\P21\Parvalbumin")


def candidate_prediction_stems(slice_filename: str) -> list[str]:
    stem = Path(slice_filename).stem
    stems = [stem]

    if stem.endswith("_thumbnail"):
        stems.append(stem.removesuffix("_thumbnail"))

    return stems


def delete_matching_prediction_files(slice_filename: str, predictions_dir: Path) -> list[Path]:
    deleted_files: list[Path] = []

    if not predictions_dir.exists():
        return deleted_files

    for stem in candidate_prediction_stems(slice_filename):
        for file_path in predictions_dir.glob(f"{stem}.*"):
            if file_path.is_file() and file_path not in deleted_files:
                file_path.unlink()
                deleted_files.append(file_path)

    return deleted_files


def find_anchoring_json_files(root_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in root_dir.rglob("*anchoring*.json")
        if path.is_file() and not path.stem.endswith("_mod")
    )


def process_registration_json(input_json: Path) -> tuple[int, int, int, Path]:
    output_json = input_json.with_name(f"{input_json.stem}_mod{input_json.suffix}")
    predictions_binary_dir = input_json.parent.parent / "predictions_binary"

    with input_json.open("r", encoding="utf-8") as f:
        registration_data = json.load(f)

    original_slices = registration_data.get("slices", [])
    removed_slices = [
        slice_data
        for slice_data in original_slices
        if not slice_data.get("markers")
    ]
    filtered_slices = [
        slice_data
        for slice_data in original_slices
        if slice_data.get("markers")
    ]

    registration_data["slices"] = filtered_slices

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(registration_data, f, indent=2)

    deleted_prediction_files: list[Path] = []
    for slice_data in removed_slices:
        deleted_prediction_files.extend(
            delete_matching_prediction_files(
                slice_data["filename"],
                predictions_binary_dir,
            )
        )

    return (
        len(original_slices),
        len(filtered_slices),
        len(deleted_prediction_files),
        output_json,
    )


anchoring_json_files = find_anchoring_json_files(ROOT_DIR)
if not anchoring_json_files:
    raise FileNotFoundError(f"No anchoring JSON files found in {ROOT_DIR}")


total_original_slices = 0
total_kept_slices = 0
total_deleted_prediction_files = 0

for input_json in anchoring_json_files:
    original_count, kept_count, deleted_predictions_count, output_json = process_registration_json(
        input_json
    )
    removed_count = original_count - kept_count

    total_original_slices += original_count
    total_kept_slices += kept_count
    total_deleted_prediction_files += deleted_predictions_count

    print(f"Processed: {input_json}")
    print(f"Saved cleaned JSON to: {output_json}")
    print(f"Original slices: {original_count}")
    print(f"Kept slices with markers: {kept_count}")
    print(f"Removed markerless slices: {removed_count}")
    print(f"Deleted prediction files: {deleted_predictions_count}")
    print()


print(f"Anchoring JSON files processed: {len(anchoring_json_files)}")
print(f"Total original slices: {total_original_slices}")
print(f"Total kept slices with markers: {total_kept_slices}")
print(f"Total removed markerless slices: {total_original_slices - total_kept_slices}")
print(f"Total deleted prediction files: {total_deleted_prediction_files}")
print(f"Root folder checked: {ROOT_DIR}")
