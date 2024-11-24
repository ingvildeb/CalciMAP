import sys
import os
import json

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import insert_existing_anchorings as iea

ID = "6"
age = "P120"
atlas_name = "ABA_Mouse_CCFv3_2017_25um.cutlas"
target_resolution = [428, 524, 320]

base_path = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}"
deepslice_anchoring = rf"{base_path}\mouse{ID}_jointAnchoring_ds.json"
full_anchoring_json = rf"{base_path}\mouse{ID}_joint.json"


combined_json_dict = iea.insert_existing_anchorings(deepslice_anchoring, full_anchoring_json, "mouse{ID}_jointAnchoring", atlas_name, target_resolution)

with open(rf"{base_path}\mouse{ID}_jointAnchoring.json", "w") as outfile:
    json.dump(combined_json_dict, outfile)   