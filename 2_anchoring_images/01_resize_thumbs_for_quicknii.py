import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff
import nutil_checker_functions as ncf

# List the IDs and markers with files to be renamed
ids = [617,900,124,239,251,295,390,774]
markers = ["cresyl_violet"]

# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
subjects_filtered = subjects.loc[(subjects['id'].isin(ids)) & (subjects['marker'].isin(markers))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
marker = subjects_filtered["marker"]
age = subjects_filtered["age"]

marker_shortnames = {"parvalbumin":"parv", "calbindin":"calb", "cresyl_violet":"CV"}


# Loop through IDs to create resize files
for i, m, a in zip(ID, marker, age):
    print(i,m,a)

    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"

    
    nff.write_nut_resize_file(filename = f"Mouse{i}_P{a}_{m.capitalize()}_resizeThumbs", 
                              storepath = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//", 
                              resize_input_dir = fr"{file_base_path}/thumbnails/", 
                              resize_output_dir = fr"{file_base_path}/thumbnails_for_anchoring/", 
                              resize_size = 10)
    
# Check whether all files were resized

# Provide a directory that contains all the nut files to be checked
    
nut_file_directory = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//"

# Check resize files
       
for file in files:
    print(f"Checking {os.path.basename(file)}")
    message, len_input_files, len_output_files = ncf.check_nut_resize_file(file, "png")
    print(message, f"{len_output_files} out of {len_input_files} done")

    
