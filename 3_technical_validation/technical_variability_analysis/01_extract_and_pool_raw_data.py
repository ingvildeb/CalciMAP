from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = "Arial"
plt.rcParams["svg.fonttype"] = "none"


ROOT_DIRS = {
    "calbindin": Path(r"D:\CalciMAP\P21\Calbindin"),
    "parvalbumin": Path(r"D:\CalciMAP\P21\Parvalbumin"),
}

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
RAW_DATA_DIR = OUTPUT_DIR / "extracted_raw_data"
RAW_SECTION_DISTRIBUTION_DIR = OUTPUT_DIR / "raw_section_distributions"
COUNT_DISTRIBUTION_DIR = RAW_SECTION_DISTRIBUTION_DIR / "counts"
DENSITY_DISTRIBUTION_DIR = RAW_SECTION_DISTRIBUTION_DIR / "densities"
METADATA_DIR = BASE_DIR / "metadata"
IMMUNOSTAINING_METADATA_PATH = METADATA_DIR / "immunostaining_metadata.csv"

REPORTS_SUBPATH = Path("nutil_output/Reports/RefAtlasRegions")
EXCLUDED_SUBJECT_NUMBERS = {"558"}

ROLLING_WINDOW_SIZE = 3
DENSITY_DIP_THRESHOLD = 0.35
DENSITY_SPIKE_THRESHOLD = 2.5
MIN_LOCAL_MEDIAN_DENSITY = 1e-9

PIXEL_SIZE_UM = 2.2
PIXEL_AREA_UM2 = PIXEL_SIZE_UM ** 2
PIXEL_AREA_MM2 = PIXEL_AREA_UM2 / 1_000_000

ANALYSIS_REGION_MAP = {
    "Basolateral amygdalar nucleus": [
        "Basolateral amygdalar nucleus, anterior part",
        "Basolateral amygdalar nucleus, posterior part",
        "Basolateral amygdalar nucleus, ventral part",
    ],
    "Anterior cingulate area": [
        "Anterior cingulate area, dorsal part, layer 1",
        "Anterior cingulate area, dorsal part, layer 2/3",
        "Anterior cingulate area, dorsal part, layer 5",
        "Anterior cingulate area, dorsal part, layer 6a",
        "Anterior cingulate area, dorsal part, layer 6b",
        "Anterior cingulate area, ventral part",
        "Anterior cingulate area, ventral part, layer 1",
        "Anterior cingulate area, ventral part, layer 2/3",
        "Anterior cingulate area, ventral part, layer 5",
        "Anterior cingulate area, ventral part, 6a",
        "Anterior cingulate area, ventral part, 6b",
    ],
    "Caudoputamen": [
        "Caudoputamen",
    ],
}
ANALYSIS_REGIONS = list(ANALYSIS_REGION_MAP.keys())
REGION_LABELS = {
    "Basolateral amygdalar nucleus": "BLA",
    "Anterior cingulate area": "ACC",
    "Caudoputamen": "CPu",
}

REGION_COLORS = {
    "Basolateral amygdalar nucleus": "#9de79c",
    "Anterior cingulate area": "#477d5b",
    "Caudoputamen": "#98d6f9",
}


def get_subject_dirs(root_dir: Path) -> list[Path]:
    return sorted(path for path in root_dir.iterdir() if path.is_dir())


def get_subject_number(subject_id: str) -> str:
    return "".join(character for character in subject_id if character.isdigit())


def is_excluded_subject(subject_id: str) -> bool:
    return subject_id in EXCLUDED_SUBJECT_NUMBERS or get_subject_number(subject_id) in EXCLUDED_SUBJECT_NUMBERS


def get_report_paths(subject_dir: Path) -> list[Path]:
    return sorted((subject_dir / REPORTS_SUBPATH).glob("RefAtlasRegions__s*.csv"))


def extract_section_number(report_path: Path) -> int:
    match = re.search(r"__s(\d+)\.csv$", report_path.name)
    if match is None:
        raise ValueError(f"Could not extract section number from {report_path.name}")
    return int(match.group(1))


def read_region_counts(report_path: Path) -> pd.DataFrame:
    section_df = pd.read_csv(report_path, sep=";")
    section_df["Object count"] = pd.to_numeric(section_df["Object count"], errors="coerce").fillna(0)
    section_df["Region area"] = pd.to_numeric(section_df["Region area"], errors="coerce").fillna(0)

    rows: list[dict[str, object]] = []
    for analysis_region, report_regions in ANALYSIS_REGION_MAP.items():
        region_df = section_df.loc[
            section_df["Region Name"].isin(report_regions),
            ["Object count", "Region area"],
        ].copy()
        object_count = float(region_df["Object count"].sum())
        region_area = float(region_df["Region area"].sum())
        density_per_mm2 = object_count / (region_area * PIXEL_AREA_MM2) if region_area > 0 else np.nan
        rows.append(
            {
                "Region Name": analysis_region,
                "Object count": object_count,
                "Region area": region_area,
                "density_per_mm2": density_per_mm2,
            }
        )

    return pd.DataFrame(rows)


def extract_subject_data(stain: str, root_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for subject_dir in get_subject_dirs(root_dir):
        subject_id = subject_dir.name
        subject_number = get_subject_number(subject_id)

        if is_excluded_subject(subject_id):
            print(f"Skipping excluded subject: {subject_id}")
            continue

        report_paths = get_report_paths(subject_dir)
        if not report_paths:
            print(f"No section reports found for {subject_id} in {subject_dir / REPORTS_SUBPATH}")
            continue

        for report_path in report_paths:
            section_number = extract_section_number(report_path)
            region_df = read_region_counts(report_path)

            for _, row in region_df.iterrows():
                rows.append(
                    {
                        "stain": stain,
                        "subject_id": subject_id,
                        "subject_number": subject_number,
                        "section_number": section_number,
                        "region_name": row["Region Name"],
                        "object_count": int(row["Object count"]),
                        "region_area": float(row["Region area"]),
                        "density_per_mm2": float(row["density_per_mm2"]) if pd.notna(row["density_per_mm2"]) else np.nan,
                        "report_path": str(report_path),
                    }
                )

    return pd.DataFrame(rows)


def summarize_by_subject(section_df: pd.DataFrame) -> pd.DataFrame:
    subject_df = (
        section_df.groupby(["stain", "subject_id", "subject_number", "region_name"], as_index=False)[["object_count", "region_area"]]
        .sum()
        .rename(columns={"object_count": "total_object_count", "region_area": "total_region_area"})
    )
    subject_df["density_per_mm2"] = np.where(
        subject_df["total_region_area"] > 0,
        subject_df["total_object_count"] / (subject_df["total_region_area"] * PIXEL_AREA_MM2),
        np.nan,
    )
    return subject_df


def attach_immunostaining_metadata(subject_df: pd.DataFrame) -> pd.DataFrame:
    if not IMMUNOSTAINING_METADATA_PATH.exists():
        print(f"No immunostaining metadata file found at: {IMMUNOSTAINING_METADATA_PATH}")
        subject_df["immunostaining_by"] = "Unknown"
        return subject_df

    metadata_df = pd.read_csv(IMMUNOSTAINING_METADATA_PATH)
    metadata_df = metadata_df.copy()
    metadata_df["subject_number"] = metadata_df["subject_number"].astype(str).str.strip()
    metadata_df["stain"] = metadata_df["stain"].astype(str).str.strip().str.lower()
    metadata_df["immunostaining_by"] = metadata_df["immunostaining_by"].astype(str).str.strip()
    metadata_df = metadata_df.drop_duplicates(subset=["subject_number", "stain"])

    merged_df = subject_df.merge(metadata_df, on=["subject_number", "stain"], how="left")
    merged_df["immunostaining_by"] = merged_df["immunostaining_by"].fillna("Unknown")
    return merged_df


def make_subject_section_plot(
    section_df: pd.DataFrame,
    stain: str,
    subject_id: str,
    output_path: Path,
    value_column: str,
    y_label: str,
    title_suffix: str,
) -> None:
    subject_section_df = section_df.loc[
        (section_df["stain"] == stain) & (section_df["subject_id"] == subject_id)
    ].copy()
    subject_section_df["region_name"] = pd.Categorical(subject_section_df["region_name"], categories=ANALYSIS_REGIONS, ordered=True)
    subject_section_df = subject_section_df.sort_values(["region_name", "section_number"])

    fig, ax = plt.subplots(figsize=(12, 7))
    for region_name in ANALYSIS_REGIONS:
        region_df = subject_section_df.loc[subject_section_df["region_name"] == region_name]
        ax.plot(
            region_df["section_number"],
            region_df[value_column],
            marker="o",
            markersize=4,
            linewidth=1.9,
            linestyle="-",
            color=REGION_COLORS.get(region_name, "#1f1f1f"),
            label=region_name,
        )

    ax.set_title(f"{stain.capitalize()} {title_suffix} for {subject_id}", fontsize=17, pad=14, fontweight="bold")
    ax.set_xlabel("Section number", fontsize=18)
    ax.set_ylabel(y_label, fontsize=18)
    ax.tick_params(axis="both", labelsize=16)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, fontsize=18)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def flag_density_outliers(section_df: pd.DataFrame) -> pd.DataFrame:
    flagged_groups: list[pd.DataFrame] = []
    for _, group_df in section_df.groupby(["stain", "subject_id", "region_name"], sort=False):
        group_df = group_df.sort_values("section_number").copy()
        local_median = group_df["density_per_mm2"].rolling(window=ROLLING_WINDOW_SIZE, center=True, min_periods=2).median()
        density_ratio = group_df["density_per_mm2"] / local_median
        group_df["local_density_median"] = local_median
        group_df["density_vs_local_median"] = density_ratio
        group_df["density_flag"] = ""

        dip_mask = (
            group_df["local_density_median"].gt(MIN_LOCAL_MEDIAN_DENSITY)
            & group_df["density_vs_local_median"].lt(DENSITY_DIP_THRESHOLD)
        )
        spike_mask = (
            group_df["local_density_median"].gt(MIN_LOCAL_MEDIAN_DENSITY)
            & group_df["density_vs_local_median"].gt(DENSITY_SPIKE_THRESHOLD)
        )
        group_df.loc[dip_mask, "density_flag"] = "dip"
        group_df.loc[spike_mask, "density_flag"] = "spike"
        flagged_groups.append(group_df)

    flagged_df = pd.concat(flagged_groups, ignore_index=True)
    return flagged_df.loc[flagged_df["density_flag"] != ""].copy()


def save_section_distribution_plots(section_df: pd.DataFrame) -> None:
    for stain in sorted(section_df["stain"].unique()):
        for subject_id in sorted(section_df.loc[section_df["stain"] == stain, "subject_id"].unique()):
            count_output_path = COUNT_DISTRIBUTION_DIR / f"{stain}_{subject_id}_count_distribution.svg"
            density_output_path = DENSITY_DISTRIBUTION_DIR / f"{stain}_{subject_id}_density_distribution.svg"

            make_subject_section_plot(
                section_df, stain, subject_id, count_output_path, "object_count", "Object count per section", "section count distribution"
            )
            print(f"Saved section distribution plot: {count_output_path}")

            make_subject_section_plot(
                section_df, stain, subject_id, density_output_path, "density_per_mm2", "Density per mm²", "section density distribution"
            )
            print(f"Saved section distribution plot: {density_output_path}")


RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
COUNT_DISTRIBUTION_DIR.mkdir(parents=True, exist_ok=True)
DENSITY_DISTRIBUTION_DIR.mkdir(parents=True, exist_ok=True)

all_section_dfs: list[pd.DataFrame] = []
for stain, root_dir in ROOT_DIRS.items():
    if not root_dir.exists():
        raise FileNotFoundError(f"Root folder does not exist: {root_dir}")
    stain_section_df = extract_subject_data(stain, root_dir)
    if stain_section_df.empty:
        print(f"No data extracted for {stain}")
        continue
    all_section_dfs.append(stain_section_df)

if not all_section_dfs:
    raise FileNotFoundError("No pooled-region data were extracted from any subject folders.")

base_section_df = pd.concat(all_section_dfs, ignore_index=True)
flagged_sections_df = flag_density_outliers(base_section_df)
subject_df = attach_immunostaining_metadata(summarize_by_subject(base_section_df))

section_output_path = RAW_DATA_DIR / "pooled_data_per_section_raw.csv"
subject_output_path = RAW_DATA_DIR / "pooled_data_per_subject_raw.csv"
flagged_sections_output_path = RAW_DATA_DIR / "flagged_sections.csv"

base_section_df.to_csv(section_output_path, index=False)
subject_df.to_csv(subject_output_path, index=False)
flagged_sections_df.to_csv(flagged_sections_output_path, index=False)

print(f"Saved raw per-section data to: {section_output_path}")
print(f"Saved raw per-subject data to: {subject_output_path}")
print(f"Saved flagged sections to: {flagged_sections_output_path}")

save_section_distribution_plots(base_section_df)
