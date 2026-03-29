from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = "Arial"
plt.rcParams["svg.fonttype"] = "none"


BASE_DIR = Path(__file__).resolve().parent
METADATA_DIR = BASE_DIR / "metadata"
OUTPUT_DIR = BASE_DIR / "output"
RAW_DATA_DIR = OUTPUT_DIR / "extracted_raw_data"
VALIDATED_DATA_DIR = OUTPUT_DIR / "validated_data"
REGIONWISE_PLOTS_DIR = OUTPUT_DIR / "regionwise_plots"

RAW_SECTION_PATH = RAW_DATA_DIR / "pooled_data_per_section_raw.csv"
VALIDATED_FLAGS_PATH = METADATA_DIR / "flagged_sections_validated.csv"
IMMUNOSTAINING_METADATA_PATH = METADATA_DIR / "immunostaining_metadata.csv"

PIXEL_SIZE_UM = 2.2
PIXEL_AREA_UM2 = PIXEL_SIZE_UM ** 2
PIXEL_AREA_MM2 = PIXEL_AREA_UM2 / 1_000_000

ANALYSIS_REGIONS = [
    "Basolateral amygdalar nucleus",
    "Anterior cingulate area",
    "Caudoputamen",
]
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

INVESTIGATOR_PALETTE = [
    "#d3e0ec",
    "#a2a7ee",
    "#7a62b3",
    "#30015f",
]


def investigator_sort_key(name: str) -> tuple[int, str]:
    match = re.search(r"(\d+)$", str(name))
    if match is not None:
        return (int(match.group(1)), str(name))
    return (10**9, str(name))


def summarize_by_subject(section_df: pd.DataFrame) -> pd.DataFrame:
    subject_df = (
        section_df.groupby(["stain", "subject_id", "subject_number", "region_name"], as_index=False)[["object_count", "region_area"]]
        .sum()
        .rename(columns={"object_count": "total_object_count", "region_area": "total_region_area"})
    )
    subject_df["subject_number"] = subject_df["subject_number"].astype(str).str.strip()
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


def exclude_validated_sections(section_df: pd.DataFrame) -> pd.DataFrame:
    if not VALIDATED_FLAGS_PATH.exists():
        raise FileNotFoundError(f"Validated flagged-sections file not found: {VALIDATED_FLAGS_PATH}")

    validated_df = pd.read_csv(VALIDATED_FLAGS_PATH)
    if "exclude" not in validated_df.columns:
        raise ValueError("Validated flagged-sections file is missing required column 'exclude'.")

    exclude_mask = validated_df["exclude"].astype(str).str.strip().str.lower().eq("yes")
    excluded_sections_df = validated_df.loc[exclude_mask].copy()
    if excluded_sections_df.empty:
        return section_df.copy()

    merge_columns = ["stain", "subject_id", "section_number", "region_name"]
    excluded_sections_df = excluded_sections_df[merge_columns].drop_duplicates()
    filtered_df = section_df.merge(
        excluded_sections_df.assign(excluded_validated=True),
        on=merge_columns,
        how="left",
    )
    filtered_df = filtered_df.loc[filtered_df["excluded_validated"] != True].copy()
    return filtered_df.drop(columns="excluded_validated")


def summarize_exclusions(raw_section_df: pd.DataFrame, validated_section_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw_noncombined_df = raw_section_df.loc[raw_section_df["region_area"] > 0].copy()
    validated_noncombined_df = validated_section_df.loc[validated_section_df["region_area"] > 0].copy()

    raw_noncombined_df["region_section_id"] = raw_noncombined_df["region_name"] + "__s" + raw_noncombined_df["section_number"].astype(str)
    validated_noncombined_df["region_section_id"] = (
        validated_noncombined_df["region_name"] + "__s" + validated_noncombined_df["section_number"].astype(str)
    )

    subject_total_df = (
        raw_noncombined_df.groupby(["stain", "subject_id"], as_index=False)["region_section_id"]
        .nunique()
        .rename(columns={"region_section_id": "n_region_sections_total"})
    )
    subject_kept_df = (
        validated_noncombined_df.groupby(["stain", "subject_id"], as_index=False)["region_section_id"]
        .nunique()
        .rename(columns={"region_section_id": "n_region_sections_kept"})
    )
    subject_exclusion_df = subject_total_df.merge(subject_kept_df, on=["stain", "subject_id"], how="left")
    subject_exclusion_df["n_region_sections_kept"] = subject_exclusion_df["n_region_sections_kept"].fillna(0).astype(int)
    subject_exclusion_df["n_region_sections_excluded"] = (
        subject_exclusion_df["n_region_sections_total"] - subject_exclusion_df["n_region_sections_kept"]
    )
    subject_exclusion_df["fraction_region_sections_excluded"] = np.where(
        subject_exclusion_df["n_region_sections_total"] > 0,
        subject_exclusion_df["n_region_sections_excluded"] / subject_exclusion_df["n_region_sections_total"],
        np.nan,
    )

    region_total_df = (
        raw_noncombined_df.groupby(["stain", "subject_id", "region_name"], as_index=False)["section_number"]
        .nunique()
        .rename(columns={"section_number": "n_sections_total"})
    )
    region_kept_df = (
        validated_noncombined_df.groupby(["stain", "subject_id", "region_name"], as_index=False)["section_number"]
        .nunique()
        .rename(columns={"section_number": "n_sections_kept"})
    )
    region_exclusion_df = region_total_df.merge(region_kept_df, on=["stain", "subject_id", "region_name"], how="left")
    region_exclusion_df["n_sections_kept"] = region_exclusion_df["n_sections_kept"].fillna(0).astype(int)
    region_exclusion_df["n_sections_excluded"] = region_exclusion_df["n_sections_total"] - region_exclusion_df["n_sections_kept"]
    region_exclusion_df["fraction_sections_excluded"] = np.where(
        region_exclusion_df["n_sections_total"] > 0,
        region_exclusion_df["n_sections_excluded"] / region_exclusion_df["n_sections_total"],
        np.nan,
    )

    return subject_exclusion_df, region_exclusion_df


def build_investigator_color_map(subject_df: pd.DataFrame) -> dict[str, str]:
    investigator_names = sorted(subject_df["immunostaining_by"].dropna().unique(), key=investigator_sort_key)
    return {
        investigator_name: INVESTIGATOR_PALETTE[index % len(INVESTIGATOR_PALETTE)]
        for index, investigator_name in enumerate(investigator_names)
    }


def make_regionwise_plot(
    subject_df: pd.DataFrame,
    stain: str,
    output_path: Path,
    value_column: str,
    y_label: str,
    investigator_colors: dict[str, str],
) -> None:
    stain_df = subject_df.loc[subject_df["stain"] == stain].copy()
    stain_df["region_name"] = pd.Categorical(stain_df["region_name"], categories=ANALYSIS_REGIONS, ordered=True)
    stain_df = stain_df.sort_values(["region_name", "subject_id"])

    fig, ax = plt.subplots(figsize=(12, 7))
    medians = stain_df.groupby("region_name", observed=False)[value_column].median().reindex(ANALYSIS_REGIONS)
    x_positions = np.arange(len(ANALYSIS_REGIONS))
    median_color = "#474747"
    investigator_names = sorted(stain_df["immunostaining_by"].dropna().unique(), key=investigator_sort_key)

    boxplot_values = [
        stain_df.loc[stain_df["region_name"] == region_name, value_column].dropna().to_numpy()
        for region_name in ANALYSIS_REGIONS
    ]

    boxplot = ax.boxplot(
        boxplot_values,
        positions=x_positions,
        widths=0.55,
        patch_artist=True,
        showfliers=False,
        boxprops={"edgecolor": "black", "linewidth": 1.2, "alpha": 0.45},
        whiskerprops={"color": "black", "linewidth": 1.2},
        capprops={"color": "black", "linewidth": 1.2},
        medianprops={"color": median_color, "linewidth": 2},
    )

    for patch, region_name in zip(boxplot["boxes"], ANALYSIS_REGIONS):
        patch.set_facecolor(REGION_COLORS.get(region_name, "#d9d9d9"))

    rng = np.random.default_rng(42)
    for x_position, region_name in zip(x_positions, ANALYSIS_REGIONS):
        region_value_df = stain_df.loc[
            stain_df["region_name"] == region_name,
            [value_column, "immunostaining_by"],
        ].dropna(subset=[value_column])
        jitter = rng.uniform(-0.12, 0.12, size=len(region_value_df))

        for point_index, (_, row) in enumerate(region_value_df.reset_index(drop=True).iterrows()):
            ax.scatter(
                x_position + jitter[point_index],
                row[value_column],
                color=investigator_colors.get(row["immunostaining_by"], "#1f1f1f"),
                s=40,
                alpha=1,
                edgecolors="black",
                linewidths=0.6,
                zorder=3,
            )

        median_value = medians.loc[region_name]
        if pd.notna(median_value):
            ax.scatter(x_position, median_value, color=median_color, marker="_", s=800, linewidths=2.5, zorder=4)

    ax.set_title(f"{stain.capitalize()} {y_label.lower()} across subjects", fontsize=17, pad=14, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=18)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([REGION_LABELS.get(region_name, region_name) for region_name in ANALYSIS_REGIONS], fontsize=16)
    ax.tick_params(axis="y", labelsize=16)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    box_handle = plt.Line2D([0], [0], color="#b8b8b8", lw=10, alpha=0.45, label="IQR")
    median_handle = plt.Line2D([0], [0], marker="_", color=median_color, markersize=18, lw=0, label="Median")
    investigator_handles = [
        plt.Line2D(
            [0], [0], marker="o", color="w",
            markerfacecolor=investigator_colors[investigator_name],
            markeredgecolor="black", markeredgewidth=0.6, markersize=7, label=investigator_name,
        )
        for investigator_name in investigator_names
    ]
    ax.legend(handles=[box_handle, median_handle] + investigator_handles, frameon=False, loc="upper left", fontsize=18)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


VALIDATED_DATA_DIR.mkdir(parents=True, exist_ok=True)
REGIONWISE_PLOTS_DIR.mkdir(parents=True, exist_ok=True)

if not RAW_SECTION_PATH.exists():
    raise FileNotFoundError(f"Raw per-section data not found: {RAW_SECTION_PATH}")

raw_section_df = pd.read_csv(RAW_SECTION_PATH)
validated_section_df = exclude_validated_sections(raw_section_df)
validated_subject_df = attach_immunostaining_metadata(summarize_by_subject(validated_section_df))
subject_exclusion_summary_df, region_exclusion_summary_df = summarize_exclusions(raw_section_df, validated_section_df)

validated_section_output_path = VALIDATED_DATA_DIR / "pooled_data_per_section_validated.csv"
validated_subject_output_path = VALIDATED_DATA_DIR / "pooled_data_per_subject_validated.csv"
subject_exclusion_output_path = VALIDATED_DATA_DIR / "region_exclusion_summary_by_subject.csv"
region_exclusion_output_path = VALIDATED_DATA_DIR / "region_exclusion_summary_by_subject_and_region.csv"

validated_section_df.to_csv(validated_section_output_path, index=False)
validated_subject_df.to_csv(validated_subject_output_path, index=False)
subject_exclusion_summary_df.to_csv(subject_exclusion_output_path, index=False)
region_exclusion_summary_df.to_csv(region_exclusion_output_path, index=False)

print(f"Saved validated per-section data to: {validated_section_output_path}")
print(f"Saved validated per-subject data to: {validated_subject_output_path}")
print(f"Saved subject exclusion summary to: {subject_exclusion_output_path}")
print(f"Saved subject-region exclusion summary to: {region_exclusion_output_path}")

investigator_colors = build_investigator_color_map(validated_subject_df)

for stain in sorted(validated_subject_df["stain"].unique()):
    count_plot_output_path = REGIONWISE_PLOTS_DIR / f"{stain}_object_counts_validated.svg"
    density_plot_output_path = REGIONWISE_PLOTS_DIR / f"{stain}_density_per_mm2_validated.svg"

    make_regionwise_plot(validated_subject_df, stain, count_plot_output_path, "total_object_count", "Total object count across sections", investigator_colors)
    print(f"Saved regionwise plot: {count_plot_output_path}")

    make_regionwise_plot(validated_subject_df, stain, density_plot_output_path, "density_per_mm2", "Density per mm²", investigator_colors)
    print(f"Saved regionwise plot: {density_plot_output_path}")
