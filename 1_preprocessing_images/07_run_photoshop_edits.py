from photoshop import Session
import photoshop.api as ps
import glob
import os
import re
import shutil
import pandas as pd


# List the IDs and markers with files to be renamed
ids = [704]
markers = ["calbindin"]

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

    tif_path = rf"{file_base_path}2_TIF\photoshop//"
    out_path = rf"{file_base_path}2_TIF\photoshop/photoshopped//"
    done_path = rf"{file_base_path}2_TIF\photoshop/origs//"

    tifs = glob.glob(rf"{tif_path}*.tif")
    tifs.extend(glob.glob(rf"{tif_path}*.tiff"))
    names = [os.path.basename(tif) for tif in tifs]

    for name in names:
    
        ID = name.split("_")[0]
        snum = re.findall("[s][0-9][0-9][0-9]", name)
        
        
        if len(snum) > 1:
            print("error: more than one potential section number in file name!")
            break
        
        elif len(snum) == 0:
            print("error: no section number in file name! please ensure section numbers are provided in the format sXXX.")
        
        else:
            path = rf"{tif_path}{name}"
            outPath = rf"{out_path}{name}"
        
            with Session(path, action="open") as ps:
                ps.app.preferences.rulerUnits = ps.Units.Percent
                ps.app.doAction(action=snum[0], action_from=f"{ID}_{marker_short}")
                options = ps.TiffSaveOptions()
                options.imageCompression = 2
                doc = ps.active_document
                doc.saveAs(outPath, options, True)
            
            shutil.move(path, done_path)