
import shutil
import pandas as pd

# List the IDs and markers with files to be renamed
ids = [110]
markers = ["calbindin"]

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
    marker_short = marker_shortnames.get(m)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    final_anchoring_path = fr"{file_base_path}/thumbnails_for_anchoring//"
    json_path = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"
    anchoring_json = rf"{json_path}\mouse{i}_anchoring_{marker_short}.json"
    shutil.copy(anchoring_json, f"{final_anchoring_path}mouse{i}_anchoring_{marker_short}.json")
