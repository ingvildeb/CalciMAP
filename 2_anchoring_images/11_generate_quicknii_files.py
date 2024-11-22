import sys
import os
import pandas as pd
from PIL import Image 
import glob
import re
import json

# List the IDs and markers with files to be copied
ids = [124]
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
template_ages = [4,7,14,21,28]

# The base path for all subfolders
base_path =r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\QuickNII_registration_workspace\\"


for i, m, a in zip(ID, marker, age):
    print(i,m,a)
    
    if a in template_ages:
        template = "template"
    else:
        template = "model"
    
    print(i, a, template)
    
    files_path = rf"{basePath}P{a}\Mouse{i}\\"
    files = glob.glob(f"{files_path}*.png")
    
    slice_dicts = []
    
    for file in files:
        img = Image.open(file) 
          
        width = img.width 
        height = img.height 
        filename = os.path.basename(file)
        nr = re.findall("[s][0-9][0-9][0-9]", filename)
        
        if len(nr) > 1:
            print("error: more than one potential section number in file name!")
            break
        else:
            nr = nr[0]
            nr = re.sub("[s]", "", nr)
            nr = int(nr)
            print(nr)
    
        slice_dict = {"nr":nr, 
                     "width":width,
                     "height":height,
                     "filename":filename}
        
        slice_dicts.append(slice_dict)

    
    sorted_slices_dicts = sorted(sliceDicts, key=lambda x: (x['nr']))
    
    if a == "120":
        json_dict = {"name":f"{ID}_jointAnchoring","target":"ABA_Mouse_CCFv3_2017_25um.cutlas","target-resolution":[428,524,320],"slices":sorted_slices_dicts}

    else:                                            
        json_dict = {"name":f"{ID}_jointAnchoring","target":f"DeMBAv2_{a}_{template}.cutlas","target-resolution":[570,705,400],"slices":sorted_slices_dicts}
    
    
    with open(rf"{basePath}P{a}\Mouse{i}\Mouse{i}_joint.json", "w") as outfile:
        json.dump(json_dict, outfile)   