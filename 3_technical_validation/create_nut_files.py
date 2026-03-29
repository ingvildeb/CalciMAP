import sys
import os
import pandas as pd
from pathlib import Path

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff


stain = "parvalbumin"

if stain == "calbindin":
    parent_dir = r"D:\CalciMAP\P21\Calbindin"
    stain_short = "calb"
elif stain == "parvalbumin":
    parent_dir = r"D:\CalciMAP\P21\Parvalbumin"
    stain_short = "parv"


for folder in Path(parent_dir).iterdir():
    subject_id = folder.name
    print(subject_id)
    atlas_dir = folder / "atlas_maps"
    seg_dir = folder / "predictions_binary"
    json_path = folder / rf"thumbnails_for_anchoring/{subject_id.lower()}_anchoring_{stain_short}.json"
    output_dir = folder / "nutil_output"
    filename = f"{subject_id}_{stain_short}_quantifier"
    nff.write_nut_quant_file(filename, str(output_dir), nut_type = "Quantifier", name = "", analysis_type = "QUINT", quantifier_input_dir = seg_dir, 
                   quantifier_atlas_dir = atlas_dir, label_file = "Developmental Mouse Brain Atlas (DeMBA)", custom_label_file = "",
                   xml_anchor_file = json_path, quantifier_output_dir = output_dir, output_report = "All", 
                   extraction_color = "255,255,255,255", 
                   object_splitting = "No", object_min_size = "1", global_pixel_scale = "1", quantifier_pixel_scale_unit = "pixels", 
                   use_custom_masks = "No", custom_mask_directory = "", custom_mask_color = "255,255,255,255", 
                   output_report_type = "CSV", 
                   custom_region_type = "Default", custom_region_file = "", coordinate_extraction = "None", pixel_density = "1", 
                   display_label_id = "No", output_region_id = "Yes", pattern_match = "_sXXX", files = "", nutil_version = "v1.0.5")
