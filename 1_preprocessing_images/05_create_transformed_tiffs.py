import sys
import os

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff

# List the IDs and markers with files to be renamed
ids = [704]
markers = ["parvalbumin", "calbindin", "cresyl_violet"]

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
    marker_short = marker_shortnames.get(m)
    
    transform_sheet = rf"{file_base_path}/mouse{i}_P{a}_{s}_{marker_short}_transform_final.xlsx"
    nut_file_string = nff.list_from_transform_sheet(transform_sheet)


    nff.write_nut_transform_file(f"Mouse{i}_P{a}_{m.capitalize()}_transform", 
                                 r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\Transform\\", 
                                 transform_input_dir = rf"{file_base_path}1_original_tiffs/", 
                                 transform_output_dir = rf"{file_base_path}2_tiffs_rotated_renamed/", 
                                 transform_files = ",".join(nut_file_string), 
                                 transform_thumbnail_size = "0.2")