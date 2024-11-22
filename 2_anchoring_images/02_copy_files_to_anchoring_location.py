import sys
import os
import pandas as pd

# List the IDs and markers with files to be copied
ids = [124,239,251,295,390,774,988]
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


# Copy all resized files to a common anchoring location across stains

for i, m, a in zip(ID, marker, age):
    print(i,m,a)
    
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    thumbs_path = fr"{file_base_path}/thumbnails_for_anchoring//"
    anchoring_path = fr"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"
    
    if m == "perineuronal_nets":
        all_thumbs = glob(thumbs_path + "*_PNN-PV_*.png")
    
    else:
        all_thumbs = glob(thumbs_path + "*.png")
    
    for thumb in allThumbs:
        name = os.path.basename(thumb)
        #print(f"copying {thumb}, to {anchoring_path}{name}")
        shutil.copy(thumb, f"{anchoring_path}{name}")