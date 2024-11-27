import sys
import os
import pandas as pd
import glob
import shutil

# List the IDs and markers with files to be copied
ids = [255,704,276]
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

marker_shortnames = {"parvalbumin":"parv", "calbindin":"calb", "cresyl_violet":"CV"}


# Copy all resized files to a common anchoring location across stains

for i, m, a in zip(ID, marker, age):
    print(i,m,a)
    
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    thumbs_path = fr"{file_base_path}/thumbnails_for_anchoring//"
    anchoring_path = fr"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"
    
    all_thumbs = glob.glob(thumbs_path + "*.png")
    
    if os.path.exists(anchoring_path):

        for thumb in all_thumbs:
            name = os.path.basename(thumb)
            shutil.copy(thumb, f"{anchoring_path}{name}")

    else:
        os.mkdir(anchoring_path)
        anchoring_path = fr"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"

        for thumb in all_thumbs:
            name = os.path.basename(thumb)
            shutil.copy(thumb, f"{anchoring_path}{name}")