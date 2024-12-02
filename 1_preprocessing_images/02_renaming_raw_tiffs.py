import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import file_naming_functions as fnf

# List the IDs and markers with files to be renamed
ids = [817]
markers = ["parvalbumin"]

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

# Loop through IDs to create renaming scheme
for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    marker_short = marker_shortnames.get(m)

    origNameList,newNameList = fnf.create_renaming_scheme(rf"{file_base_path}\\1_original_tiffs\\",
                                                    rf"{file_base_path}\\",
                                                    f"mouse{i}_P{a}_{s}_{marker_short}",
                                                    maxScenes = 3,
                                                    underscores = 3)

# Check for any duplicate names in renaming scheme
for i, m, a, s in zip(ID, marker, age, sex):
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    marker_short = marker_shortnames.get(m)

    fnf.find_duplicate_names(rf"{file_base_path}\\mouse{i}_P{a}_{s}_{marker_short}_renamingScheme.xlsx")


for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    marker_short = marker_shortnames.get(m)

    #rename tiffs
    fnf.rename_files(rf"{file_base_path}\\1_original_tiffs\\",
                rf"{file_base_path}\\mouse{i}_P{a}_{s}_{marker_short}_renamingScheme.xlsx")