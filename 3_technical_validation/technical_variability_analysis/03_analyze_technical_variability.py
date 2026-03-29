from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu

plt.rcParams["font.family"] = "Arial"
plt.rcParams["svg.fonttype"] = "none"


BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "output" / "validated_data" / "pooled_data_per_subject_validated.csv"
OUTPUT_DIR = BASE_DIR / "output" / "investigator_variability"
PLOT_DIR = OUTPUT_DIR / "density_plots"

INVESTIGATOR_PALETTE = [
    "#d3e0ec",
    "#a2a7ee",
    "#7a62b3",
    "#30015f",
]
VALUE_COLUMN = "density_per_mm2"
Y_LABEL = "Density per mm²"


def investigator_sort_key(name: str) -> tuple[int, str]:
    match = re.search(r"(\d+)$", str(name))
    if match is not None:
        return (int(match.group(1)), str(name))
    return (10**9, str(name))


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    if not p_values:
        return []

    p_values_array = np.asarray(p_values, dtype=float)
    n_tests = len(p_values_array)
    ranked_indices = np.argsort(p_values_array)
    ranked_p_values = p_values_array[ranked_indices]

    adjusted_ranked = np.empty(n_tests, dtype=float)
    running_min = 1.0
    for index in range(n_tests - 1, -1, -1):
        rank = index + 1
        adjusted_value = ranked_p_values[index] * n_tests / rank
        running_min = min(running_min, adjusted_value)
        adjusted_ranked[index] = running_min

    adjusted_p_values = np.empty(n_tests, dtype=float)
    adjusted_p_values[ranked_indices] = np.clip(adjusted_ranked, 0, 1)
    return adjusted_p_values.tolist()


def run_group_test(group_df: pd.DataFrame) -> tuple[str, float]:
    grouped_values = []
    for _, subgroup_df in group_df.groupby("immunostaining_by", sort=True):
        values = subgroup_df[VALUE_COLUMN].dropna().to_numpy()
        if len(values) > 0:
            grouped_values.append(values)

    if len(grouped_values) < 2:
        return "not_tested", np.nan
    if len(grouped_values) == 2:
        _, p_value = mannwhitneyu(grouped_values[0], grouped_values[1], alternative="two-sided")
        return "mannwhitneyu", float(p_value)

    _, p_value = kruskal(*grouped_values)
    return "kruskal", float(p_value)


def summarize_groups(group_df: pd.DataFrame) -> str:
    summary_parts: list[str] = []
    for group_name, subgroup_df in group_df.groupby("immunostaining_by", sort=True):
        values = subgroup_df[VALUE_COLUMN].dropna().to_numpy()
        if len(values) == 0:
            continue
        summary_parts.append(
            f"{group_name}: n={len(values)}, median={np.median(values):.3f}, mean={np.mean(values):.3f}"
        )
    return " | ".join(summary_parts)


def build_investigator_color_map(subject_df: pd.DataFrame) -> dict[str, str]:
    investigator_names = sorted(subject_df["immunostaining_by"].dropna().unique(), key=investigator_sort_key)
    return {
        investigator_name: INVESTIGATOR_PALETTE[index % len(INVESTIGATOR_PALETTE)]
        for index, investigator_name in enumerate(investigator_names)
    }


def make_group_plot(
    group_df: pd.DataFrame,
    stain: str,
    region_name: str,
    output_path: Path,
    investigator_colors: dict[str, str],
) -> None:
    plot_df = group_df.copy()
    group_order = sorted(plot_df["immunostaining_by"].dropna().unique(), key=investigator_sort_key)
    plot_df["immunostaining_by"] = pd.Categorical(plot_df["immunostaining_by"], categories=group_order, ordered=True)
    plot_df = plot_df.sort_values(["immunostaining_by", "subject_id"])

    fig, ax = plt.subplots(figsize=(9, 6))
    x_positions = np.arange(len(group_order))
    boxplot_values = [
        plot_df.loc[plot_df["immunostaining_by"] == group_name, VALUE_COLUMN].dropna().to_numpy()
        for group_name in group_order
    ]

    boxplot = ax.boxplot(
        boxplot_values,
        positions=x_positions,
        widths=0.5,
        patch_artist=True,
        showfliers=False,
        boxprops={"edgecolor": "black", "linewidth": 1.2, "alpha": 0.5},
        whiskerprops={"color": "black", "linewidth": 1.2},
        capprops={"color": "black", "linewidth": 1.2},
        medianprops={"color": "#8f1630", "linewidth": 2},
    )

    for patch, group_name in zip(boxplot["boxes"], group_order):
        patch.set_facecolor(investigator_colors.get(group_name, "#9ab7c9"))

    rng = np.random.default_rng(42)
    for x_position, group_name in zip(x_positions, group_order):
        values = plot_df.loc[plot_df["immunostaining_by"] == group_name, VALUE_COLUMN].dropna().to_numpy()
        jitter = rng.uniform(-0.1, 0.1, size=len(values))
        ax.scatter(
            np.full(len(values), x_position) + jitter,
            values,
            color=investigator_colors.get(group_name, "#1f1f1f"),
            s=40,
            alpha=0.9,
            edgecolors="black",
            linewidths=0.6,
            zorder=3,
        )

    ax.set_title(region_name, fontsize=16, pad=12, fontweight="bold")
    ax.set_ylabel(Y_LABEL, fontsize=18)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(group_order, fontsize=16)
    ax.tick_params(axis="y", labelsize=16)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    box_handle = plt.Line2D([0], [0], color="#b8b8b8", lw=10, alpha=0.5, label="IQR")
    median_handle = plt.Line2D([0], [0], marker="_", color="#8f1630", markersize=18, lw=0, label="Median")
    ax.legend(handles=[box_handle, median_handle], frameon=False, loc="upper left", fontsize=18)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"Validated per-subject data not found: {INPUT_PATH}")

subject_df = pd.read_csv(INPUT_PATH)
subject_df["stain"] = subject_df["stain"].astype(str).str.strip().str.lower()
subject_df["region_name"] = subject_df["region_name"].astype(str).str.strip()
subject_df["subject_number"] = subject_df["subject_number"].astype(str).str.strip()
subject_df["immunostaining_by"] = subject_df["immunostaining_by"].fillna("Unknown").astype(str).str.strip()
subject_df = subject_df.loc[subject_df["immunostaining_by"] != "Unknown"].copy()

investigator_colors = build_investigator_color_map(subject_df)
all_results: list[dict[str, object]] = []

for (stain, region_name), group_df in subject_df.groupby(["stain", "region_name"], sort=True):
    test_name, p_value = run_group_test(group_df)
    group_summary = summarize_groups(group_df)
    n_subjects = int(group_df["subject_id"].nunique())
    n_groups = int(group_df["immunostaining_by"].nunique())

    all_results.append(
        {
            "stain": stain,
            "region_name": region_name,
            "value_column": VALUE_COLUMN,
            "test_name": test_name,
            "p_value": p_value,
            "n_subjects": n_subjects,
            "n_groups": n_groups,
            "group_summary": group_summary,
        }
    )

    output_path = PLOT_DIR / f"{stain}_{region_name}_{VALUE_COLUMN}_by_investigator.svg"
    make_group_plot(group_df, stain, region_name, output_path, investigator_colors)
    print(f"Saved plot: {output_path}")


results_df = pd.DataFrame(all_results)
valid_p_values_df = results_df.loc[results_df["p_value"].notna()].copy()
valid_p_values_df["p_value_fdr_bh"] = benjamini_hochberg(valid_p_values_df["p_value"].tolist())
results_df = results_df.merge(
    valid_p_values_df[["stain", "region_name", "value_column", "p_value_fdr_bh"]],
    on=["stain", "region_name", "value_column"],
    how="left",
)

results_output_path = OUTPUT_DIR / "investigator_effect_statistics.csv"
results_df.to_csv(results_output_path, index=False)
print(f"Saved statistics to: {results_output_path}")
