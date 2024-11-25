import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff

# List the IDs and markers with files to be renamed
ids = [276]
markers = ["cresyl_violet", "parvalbumin", "calbindin"]

# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
subjects_filtered = subjects.loc[(subjects['id'].isin(ids)) & (subjects['marker'].isin(markers))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
marker = subjects_filtered["marker"]
age = subjects_filtered["age"]
sex = subjects_filtered["sex"]

marker_shortnames = {"parvalbumin":"parv", "calbindin":"calb", "cresyl_violet":"CV"}


for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"

    tiff_path = fr"{file_base_path}2_TIF\photoshop\tiled\\"
    nut_file_string = nff.nut_list_from_files(tiff_path)

  
    nff.write_nut_transform_file(f"Mouse{i}_{a}_{m.capitalize()}_tiledThumbs", 
                                "Y:/2021_Bjerke_DevMouse_projects/01_DATA/Transform/", 
                                 transform_input_dir = tiff_path, 
                                 transform_output_dir = tiff_path, 
                                 transform_files = nut_file_string, 
                                 only_thumbnails = "Yes", 
                                 transform_thumbnail_size = "0.1")