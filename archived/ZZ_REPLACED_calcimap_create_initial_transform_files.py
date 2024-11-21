# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:52:19 2023

@author: ingvieb
"""

import pandas as pd
import nutil_scripts.create_nut_file_functions as nff
from glob import glob
import re

resourcedir = 'Y:/2021_Bjerke_DevMouse_projects/01_DATA//'
metadata = resourcedir + "ids_to_make_files.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]


# ID = ["Mouse2"]
# marker = ["Parvalbumin"]
# age = ["P120"]
# sex = ["F"]

# Create files with list of new file names


for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
    transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
    transformfiles = glob(transform_input_dir + "*.tif")


    file_names = []
    for f in transformfiles:
        file = f.split("\\")[-1]
        file_names.append(file)


   
    mylist = []
    
    
    for file in file_names:
        scene_list = []
        scene = (file.split(sep=".tif")[0]).split(sep="_")[-1]
        scene_list.append(scene)
           
        
        for scene in scene_list:
                
            if scene == "s1":
                section = (file.split(sep="_")[3])
                mylist.append(section)
            elif scene == "s2":
                section = (file.split(sep="_")[4])
                mylist.append(section)        
            elif scene == "s3":
                section = ((file.split(sep="_")[5])).split("-")[0]
                mylist.append(section) 
            elif scene == "s4":
                section = ((file.split(sep="_")[6])).split("-")[0]
                mylist.append(section)
            else:
                section = (file.split(sep="_")[3]).split(sep="-")[0]
                mylist.append(section)


                
    new_file_names = [] 
           
    for section in mylist:
        section = str(section)
        section = re.sub('[^0-9]','', section)
        section = section.zfill(3)
        section = "s" + section
        section = i + "_" + a + "_" + s + "_" + m + "_" + section
        section = section.replace("Mouse", "mouse")
        section = section.replace("Calbindin", "calb")
        section = section.replace("Parvalbumin", "parv")
        section = section.replace("Cresyl_violet", "CV")
        new_file_names.append(section)
        
    
    #trying to create df for nut transform input file
    df = pd.DataFrame(columns = ["Input file name", "Renamed", "Rotation CCW", "Scale X", "Scale Y"])
    df["Input file name"] = file_names
    df["Renamed"] = new_file_names
    df["Rotation CCW"] = 0
    df["Scale X"] = 1
    df["Scale Y"] = 1
    
    df.to_excel("Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_transform.xlsx", index=False)
    
    print(i + " done")
    
   
    # nff.write_nut_transform_file(i + "_" + a + "_" + m + "_transform", "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m,
    #                               transform_input_dir = transform_input_dir,
    #                               transform_output_dir = transform_output_dir,
    #                               only_thumbnails = "No",
    #                               transform_thumbnail_size = "0.1")
    
