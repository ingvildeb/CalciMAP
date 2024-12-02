import json
import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import alignment_json_utils as aju

# List the IDs and markers with files to be renamed
ids = [111]
markers = ["calbindin", "parvalbumin", "cresyl_violet"]

# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
subjects_filtered = subjects.loc[(subjects['id'].isin(ids)) & (subjects['marker'].isin(markers))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
age = subjects_filtered["age"]
ID_age_dict = dict(zip(ID,age))

ID = list(set(ID))


specific_strings = ["calb", "parv", "CV"]

for i in ID:
    a = ID_age_dict.get(i)
    print(i,a)
    json_path = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"
    json_file = rf"{json_path}mouse{i}_jointAnchoring_final_nonlinear.json"
    json_data = aju.read_json(json_file)

    for str in specific_strings:
        specific_dict = aju.split_json(json_data, str)
        specific_json = aju.create_quicknii_json_dict(json_data["name"], json_data["target"], json_data["target-resolution"])
        specific_json["slices"] = specific_dict

        with open(rf"{json_path}mouse{i}_anchoring_{str}.json", "w") as outfile:
            json.dump(specific_json, outfile)  