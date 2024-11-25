import sys
import os
import pandas as pd
from PIL import Image 
import glob
import re
import json

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import alignment_json_utils as aju

# List the IDs and markers with pngs to be made into QuickNII json
ids = [124]

# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
subjects_filtered = subjects.loc[(subjects['id'].isin(ids))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
age = subjects_filtered["age"]
ID_age_dict = dict(zip(ID,age))

ID = list(set(ID))

template_ages = [4,7,14,21,28]

# The base path for all subfolders
base_path = r"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\\"

for i in ID:
    a = ID_age_dict.get(i)

    if a in template_ages:
        template = "template"
    else:
        template = "model"
    
    print(i, a, template)
    
    files_path = rf"{base_path}P{a}\Mouse{i}\\"
    name = f"Mouse{i}_TESTTESTjointAnchoring"

    if a == "120":
        target = "ABA_Mouse_CCFv3_2017_25um.cutlas"
        target_resolution = [428,524,320]

    else:        
        target = f"DeMBAv2_P{a}_{template}.cutlas"
        target_resolution = [570,705,400]   

    aju.create_quicknii_slicedict(files_path, 
                                  rf"{files_path}{name}",
                                  name,
                                  target,
                                  target_resolution)                  
        
