from __future__ import annotations

from pathlib import Path

import numpy as np
import tifffile
from PIL import Image


SUPPORTED_EXTENSIONS = {
    ".png",
    ".tif",
    ".tiff",
    ".jpg",
    ".jpeg",
    ".bmp",
}


ROOT_DIR = Path(r"D:\CalciMAP\P21\Parvalbumin")
OVERWRITE = True


def iter_prediction_dirs(root_dir: Path) -> list[Path]:
    return sorted(
        path for path in root_dir.rglob("predictions") if path.is_dir()
    )


def iter_image_paths(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def read_image(path: Path) -> np.ndarray:
    suffix = path.suffix.lower()

    if suffix in {".tif", ".tiff"}:
        return tifffile.imread(path)

    with Image.open(path) as img:
        return np.asarray(img)


def write_image(path: Path, image: np.ndarray) -> None:
    Image.fromarray(image).save(path)


def binarize_image(image: np.ndarray) -> np.ndarray:
    mask = np.any(image > 0, axis=-1) if image.ndim == 3 else image > 0
    binary_rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
    binary_rgb[mask] = (255, 255, 255)
    return binary_rgb


def build_output_path(input_path: Path, input_dir: Path, output_dir: Path) -> Path:
    relative_path = input_path.relative_to(input_dir)
    output_name = Path(relative_path.name.removeprefix("masks_")).stem + ".png"
    return output_dir / relative_path.parent / output_name


root_dir = ROOT_DIR.expanduser().resolve()

if not root_dir.exists():
    raise FileNotFoundError(f"Root folder does not exist: {root_dir}")
if not root_dir.is_dir():
    raise NotADirectoryError(f"Root path is not a folder: {root_dir}")

prediction_dirs = iter_prediction_dirs(root_dir)
if not prediction_dirs:
    raise FileNotFoundError(f"No predictions folders found in {root_dir}")

processed = 0
skipped = 0

for input_dir in prediction_dirs:
    output_dir = input_dir.parent / "predictions_binary"
    image_paths = iter_image_paths(input_dir)

    if not image_paths:
        print(f"No supported image files found in {input_dir}")
        continue

    output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in image_paths:
        output_path = build_output_path(input_path, input_dir, output_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not OVERWRITE:
            skipped += 1
            print(f"Skipping existing file: {output_path}")
            continue

        image = read_image(input_path)
        binary_image = binarize_image(image)
        write_image(output_path, binary_image)
        processed += 1
        print(f"Binarized: {input_path} -> {output_path}")

print(
    f"Done. Processed {processed} image(s), skipped {skipped}, "
    f"across {len(prediction_dirs)} predictions folder(s) under {root_dir}"
)
