import json
import glob
import os
import sys
import pandas as pd
from PIL import Image 
import re

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import alignment_json_utils as aju

# List the IDs and markers with files to be renamed
ids = [2,3,4,6,8,9,10,11]
markers = ["calbindin", "parvalbumin"]

# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
subjects_filtered = subjects.loc[(subjects['id'].isin(ids)) & (subjects['marker'].isin(markers))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
age = subjects_filtered["age"]
marker = subjects_filtered["marker"]
sex = subjects_filtered["sex"]

marker_shortnames = {"parvalbumin":"parv", "calbindin":"calb", "cresyl_violet":"CV"}

for i, m, a, s in zip(ID, marker, age, sex):
    print(f"Checking mouse{i}, P{a}, {s}, {m}")
    marker_short = marker_shortnames.get(m)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    alignment_path = rf"{file_base_path}thumbnails_for_anchoring\\"
    json_file = rf"{alignment_path}mouse{i}_anchoring_{marker_short}.json"

    files_in_folder = glob.glob(rf"{alignment_path}*.png")
    names_in_folder = [os.path.basename(i) for i in files_in_folder]

    json_data = aju.read_json(json_file)
    names_in_json = []

    for s in json_data["slices"]:
        name = s["filename"]
        names_in_json.append(name)
    
    for name in names_in_folder:
        if name in names_in_json:
            continue
        else:
            print(rf"Error: {name} in files but not in json")

    for name in names_in_json:
        if name in names_in_folder:
            continue
        else:
            print(rf"Error: {name} in json but not in files")

    for file in files_in_folder:
        img = Image.open(file) 
          
        width = img.width 
        height = img.height 
        filename = os.path.basename(file)
        nr = re.findall("[s][0-9][0-9][0-9]", filename)
        nr = nr[0]
        nr = re.sub("[s]", "", nr)
        nr = int(nr)

        file_slice_dict = aju.get_slice_dict(nr, width, height, filename)

        for s in json_data["slices"]:
            if s["nr"] == nr:
                json_width = s["width"]
                json_height = s["height"]
                if (abs(json_width - width) <= 1) or (abs(json_height - height) <= 1):
                    continue
                else:
                    print(f"Error! Mismatching dimensions for section nr {nr}")
                    print(f"width of image is {width}, width in json is {json_width}")
                    print(f"height of image is {height}, height in json is {json_height}")

