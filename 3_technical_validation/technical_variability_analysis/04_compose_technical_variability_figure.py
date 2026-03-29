from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
REGIONWISE_PLOTS_DIR = OUTPUT_DIR / "regionwise_plots"
INVESTIGATOR_PLOTS_DIR = OUTPUT_DIR / "investigator_variability" / "density_plots"
FINAL_FIGURES_DIR = OUTPUT_DIR / "final_figures"
OUTPUT_PATH = FINAL_FIGURES_DIR / "technical_variability_figure_layout.svg"

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

TOP_ROW_PANELS = [
    ("A", "Calbindin pooled regions", REGIONWISE_PLOTS_DIR / "calbindin_density_per_mm2_validated.svg"),
    ("B", "Parvalbumin pooled regions", REGIONWISE_PLOTS_DIR / "parvalbumin_density_per_mm2_validated.svg"),
]

CALBINDIN_PANELS = [
    ("C", "Calbindin Caudoputamen", INVESTIGATOR_PLOTS_DIR / "calbindin_Caudoputamen_density_per_mm2_by_investigator.svg"),
    ("D", "Calbindin Anterior cingulate area", INVESTIGATOR_PLOTS_DIR / "calbindin_Anterior cingulate area_density_per_mm2_by_investigator.svg"),
    ("E", "Calbindin Basolateral amygdalar nucleus", INVESTIGATOR_PLOTS_DIR / "calbindin_Basolateral amygdalar nucleus_density_per_mm2_by_investigator.svg"),
]

PARVALBUMIN_PANELS = [
    ("F", "Parvalbumin Caudoputamen", INVESTIGATOR_PLOTS_DIR / "parvalbumin_Caudoputamen_density_per_mm2_by_investigator.svg"),
    ("G", "Parvalbumin Anterior cingulate area", INVESTIGATOR_PLOTS_DIR / "parvalbumin_Anterior cingulate area_density_per_mm2_by_investigator.svg"),
    ("H", "Parvalbumin Basolateral amygdalar nucleus", INVESTIGATOR_PLOTS_DIR / "parvalbumin_Basolateral amygdalar nucleus_density_per_mm2_by_investigator.svg"),
]

PAGE_WIDTH = 3600
PAGE_HEIGHT = 2800
PAGE_WIDTH_MM = 180
PAGE_HEIGHT_MM = 170
OUTER_MARGIN = 28
ROW_GAP = 24
COLUMN_GAP = 10
PANEL_LABEL_FONT_SIZE = 28
PANEL_LABEL_Y_OFFSET = 6
PANEL_LABEL_X_OFFSET = 4
LOWER_PANEL_HEIGHT = 510
TOP_ROW_HEIGHT = LOWER_PANEL_HEIGHT


def parse_viewbox(svg_root: ET.Element) -> tuple[float, float, float, float]:
    viewbox = svg_root.get("viewBox")
    if viewbox:
        min_x, min_y, width, height = (float(value) for value in viewbox.replace(",", " ").split())
        return min_x, min_y, width, height

    width_attr = svg_root.get("width", "100")
    height_attr = svg_root.get("height", "100")
    width = float(re.sub(r"[A-Za-z%]+", "", width_attr))
    height = float(re.sub(r"[A-Za-z%]+", "", height_attr))
    return 0.0, 0.0, width, height


def prefix_svg_ids(svg_root: ET.Element, prefix: str) -> ET.Element:
    svg_root = copy.deepcopy(svg_root)
    id_map: dict[str, str] = {}

    for element in svg_root.iter():
        element_id = element.get("id")
        if element_id:
            new_id = f"{prefix}_{element_id}"
            id_map[element_id] = new_id
            element.set("id", new_id)

    url_pattern = re.compile(r"url\(#([^)]+)\)")
    for element in svg_root.iter():
        for attribute_name, attribute_value in list(element.attrib.items()):
            updated_value = attribute_value
            for original_id, new_id in id_map.items():
                updated_value = updated_value.replace(f"#{original_id}", f"#{new_id}")
            updated_value = url_pattern.sub(
                lambda match: f"url(#{id_map.get(match.group(1), match.group(1))})",
                updated_value,
            )
            if attribute_name in {f"{{{XLINK_NS}}}href", "href"} and updated_value.startswith("#"):
                updated_value = f"#{id_map.get(updated_value[1:], updated_value[1:])}"
            if updated_value != attribute_value:
                element.set(attribute_name, updated_value)

    return svg_root


def append_svg_panel(
    parent: ET.Element,
    panel_label: str,
    svg_path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    if not svg_path.exists():
        raise FileNotFoundError(f"Missing SVG panel: {svg_path}")

    source_root = prefix_svg_ids(ET.parse(svg_path).getroot(), prefix=panel_label.lower())
    min_x, min_y, viewbox_width, viewbox_height = parse_viewbox(source_root)

    panel_group = ET.SubElement(parent, f"{{{SVG_NS}}}g")
    ET.SubElement(
        panel_group,
        f"{{{SVG_NS}}}text",
        {
            "x": str(x - PANEL_LABEL_X_OFFSET),
            "y": str(y - PANEL_LABEL_Y_OFFSET),
            "font-size": str(PANEL_LABEL_FONT_SIZE),
            "font-weight": "bold",
            "font-family": "Arial, Helvetica, sans-serif",
        },
    ).text = panel_label

    nested_svg = ET.SubElement(
        panel_group,
        f"{{{SVG_NS}}}svg",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "viewBox": f"{min_x} {min_y} {viewbox_width} {viewbox_height}",
            "preserveAspectRatio": "xMidYMid meet",
        },
    )
    for child in list(source_root):
        nested_svg.append(copy.deepcopy(child))


FINAL_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

canvas = ET.Element(
    f"{{{SVG_NS}}}svg",
    {
        "width": f"{PAGE_WIDTH_MM}mm",
        "height": f"{PAGE_HEIGHT_MM}mm",
        "viewBox": f"0 0 {PAGE_WIDTH} {PAGE_HEIGHT}",
        "version": "1.1",
    },
)
ET.SubElement(
    canvas,
    f"{{{SVG_NS}}}rect",
    {"x": "0", "y": "0", "width": str(PAGE_WIDTH), "height": str(PAGE_HEIGHT), "fill": "white"},
)

column_width = (PAGE_WIDTH - 2 * OUTER_MARGIN - COLUMN_GAP) / 2

for index, (panel_label, panel_title, svg_path) in enumerate(TOP_ROW_PANELS):
    append_svg_panel(
        canvas,
        panel_label,
        svg_path,
        OUTER_MARGIN + index * (column_width + COLUMN_GAP),
        OUTER_MARGIN + 18,
        column_width,
        TOP_ROW_HEIGHT,
    )

lower_start_y = OUTER_MARGIN + 18 + TOP_ROW_HEIGHT + ROW_GAP + 18

for column_index, panel_group in enumerate([CALBINDIN_PANELS, PARVALBUMIN_PANELS]):
    column_x = OUTER_MARGIN + column_index * (column_width + COLUMN_GAP)

    for row_index, (panel_label, panel_title, svg_path) in enumerate(panel_group):
        panel_y = lower_start_y + row_index * (LOWER_PANEL_HEIGHT + ROW_GAP)
        append_svg_panel(
            canvas,
            panel_label,
            svg_path,
            column_x,
            panel_y,
            column_width,
            LOWER_PANEL_HEIGHT,
        )

ET.ElementTree(canvas).write(OUTPUT_PATH, encoding="utf-8", xml_declaration=True)
print(f"Saved composed figure to: {OUTPUT_PATH}")
