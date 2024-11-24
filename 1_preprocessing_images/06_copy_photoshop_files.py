import pandas as pd
from glob import glob
import os
import re
from tqdm import tqdm
import shutil

# List the IDs and markers with files to be renamed
ids = [276]
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

for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    marker_short = marker_shortnames.get(m)
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    tif_path = rf"{file_base_path}2_TIF\\"
    
    tif_files = glob(rf"{tif_path}*.tif")

    # Set up temporary folders for Photoshopping work
    os.mkdir(rf"{tif_path}photoshop//")
    ps_dir = rf"{tif_path}photoshop//"

    os.mkdir(rf"{ps_dir}origs//")
    os.mkdir(rf"{ps_dir}photoshopped//")
    
    # Read photoshop instructions from nutil transform sheet
    ps_instructions = pd.read_excel(rf"{file_base_path}\mouse{i}_P{a}_{s}_{marker_short}_transform_final.xlsx", usecols="B,F")
    ps_instructions = ps_instructions.rename(columns={ps_instructions.columns[1]: "Photoshop"})
    ps_instructions = ps_instructions.dropna()

    identified_names =  ps_instructions["Renamed"].tolist()
    snums_to_copy = [re.findall("[s][0-9][0-9][0-9]", name)[0] for name in identified_names]
    
    copied_files = []
    for file in tqdm(tif_files):
        filename = os.path.basename(file)
        snum = re.findall("[s][0-9][0-9][0-9]", filename)[0]
        #print(filename, snum)
        
        if snum in snums_to_copy:
            print(f"{snum} being copied...")
            copied_files.append(snum)
            
            #dst = f"{ps_dir}{filename}"
            shutil.copyfile(file, f"{ps_dir}{filename}")
            
        else:
            continue