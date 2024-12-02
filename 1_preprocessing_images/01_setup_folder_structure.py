import os
import pandas as pd

# List the IDs and markers to be created folders for
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

# The base path for all subfolders
base_path =r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\\"

# Loop through IDs to create folder structure
for i, m, a in zip(ID, marker, age):
    print(i,m,a)
    path_for_folder = rf"{base_path}P{a}\\{m.capitalize()}\\"
    print(path_for_folder)

    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/")
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/1_CZI")
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/1_original_tiffs")
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/1_original_tiffs/metadata")
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/2_TIF")
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/thumbnails_for_anchoring")