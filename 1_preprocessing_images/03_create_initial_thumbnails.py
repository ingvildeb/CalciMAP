import sys
import os

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff

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


for i, m, a in zip(ID, marker, age):
    print(i,m,a)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"

    transform_dir = rf"{file_base_path}\\1_original_tiffs\\" 
    transform_files = nff.nut_list_from_files(transform_dir)

   
    nff.write_nut_transform_file(rf"Mouse{i}_P{a}_{m.capitalize()}_thumbs", "Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_IEB/",
                                 transform_input_dir = transform_dir,
                                 transform_output_dir = transform_dir,
                                 transform_files = transform_files,
                                 only_thumbnails = "Yes",
                                 transform_thumbnail_size = "0.02")