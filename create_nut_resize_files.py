# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:51:42 2024

@author: ingvieb
"""



##### MAKE NUT FILES



import pandas as pd
import nutil_scripts.create_nut_file_functions as nff
from glob import glob
import os

resourcedir = r'Y:/2021_Bjerke_DevMouse_projects/01_DATA//'
metadata = resourcedir + "ids_to_make_files.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]


for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    #os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/thumbnails_for_anchoring")

    
    resize_input_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/thumbnails/" 
    resize_output_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/thumbnails_for_anchoring/"
    
    nutil_file_name = f"{i}_{a}_{m}_resizeThumbs"
    nutil_store_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//"
    
    resize_size = 10
    
    nff.write_nut_resize_file(nutil_file_name, nutil_store_path, resize_input_dir = resize_input_dir, resize_output_dir = resize_output_dir, 
                              resize_size=resize_size)






#### CHECK THAT ALL FILES WERE MADE


import shutil
import nutil_scripts.checking_functions as ncf


nut_file_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_IEB/"
nut_files = glob(nut_file_path + "*.nut")

data_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/"

done_path = f"{nut_file_path}/done/"

for file in nut_files:
    print(file)
    filename = (file.split(sep="\\")[-1])
    ID = filename.split(sep="_", maxsplit=1)[0]
    stain = (filename.split(sep="_")[2]).split(sep="_r")[0]
    age = filename.split(sep="_")[1]
    

    if stain == "Cresyl":
        stain = "Cresyl_violet"
    else:
        stain = stain

    print(ID, stain, age)
        
    transform_path = f"{data_path}{age}/{stain}/{ID}/thumbnails/"
    thumb_path = f"{data_path}{age}/{stain}/{ID}/thumbnails_for_anchoring/"
    
    
    message = ncf.check_files_in_folders(transform_path, thumb_path, ".png", ".png")
    folder1files, folder2files = ncf.name_files_in_folders(transform_path, thumb_path, ".png", ".png")
    missing_files = ncf.identify_missing_files(folder1files, folder2files)
    print(len(folder1files), len(folder2files))

    
    if len(folder1files) == len(folder2files):
        shutil.move(file, f"{done_path}{ID}_{age}_{stain}_finalThumbs.nut")
        
        
    else:
        continue
        






###### COPY FILES TO ANCHORING LOCATION

resourcedir = r'Y:/2021_Bjerke_DevMouse_projects/01_DATA//'
metadata = resourcedir + "ids_to_make_files.xlsx"
data_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]

for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    
    thumbsDir = fr"{data_path}{a}/{m}/{i}/thumbnails_for_anchoring//"
    anchoringDir = fr"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{a}\{i}\\"
    
    if m == "Perineuronal_nets":
        allThumbs = glob(thumbsDir + "*_PNN-PV_*.png")
    
    else:
        allThumbs = glob(thumbsDir + "*.png")
    
    for thumb in allThumbs:
        #print(thumb)
        name = os.path.basename(thumb)
        #print(name)
        #print(f"copying {thumb}, to {anchoringDir}{name}")
        
        shutil.copy(thumb, f"{anchoringDir}{name}")
        




