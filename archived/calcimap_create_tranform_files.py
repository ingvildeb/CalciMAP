# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:49:57 2023

@author: ingvieb
"""

import pandas as pd
import nutil_scripts.create_nut_file_functions as nff
import nutil_scripts.checking_functions as ncf
from glob import glob
import re
import shutil
import os
import time

resourcedir = 'Y:/2021_Bjerke_DevMouse_projects/01_DATA//'
metadata = resourcedir + "ids_to_make_files.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]

# Write nut transform files from toDo sheets (filtering out ps adjustment sections):
    
for i, m, a, s in zip(ID, marker, age, sex):
    
    
    if m == "Calbindin" or m == "Parvalbumin":
        print(i,m,a,s)
        
        transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_TIF/" #"Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
        transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/temp_output/" #"Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
        transform_sheet = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_toDo.xlsx"
    
        
        filename = f"{i}_{a}_{m}_transform"
        
        nut_file_string = nff.list_from_transform_sheet(transform_sheet)
        transformed_names = []
        nut_file_string_filtered = []
        all_tifs = glob(transform_input_dir + "*.tif")
        all_tifs_names = []
        
        for file in all_tifs:
            name = (os.path.basename(file)).split(".")[0]
            all_tifs_names.append(name)
            
        for string in nut_file_string:    
            name = string.split(",")[0]
            if name not in all_tifs_names:
                print(f"Warning: {name} not in list of existing tiffs!")
                break
            else:
                continue
        
        for string in nut_file_string:
            rot = int(string.split(",")[-3])
            scale_x = int(string.split(",")[-2])
            scale_y = int(string.split(",")[-1])
            
            if (rot == 0 and scale_x == 1 and scale_y == 1):
                continue
            else:
                nut_file_string_filtered.append(string)
                transformed_names.append(name)  
        
            
        
        nff.write_nut_transform_file(filename, r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB\\", transform_input_dir = transform_input_dir, 
                                       transform_output_dir = transform_output_dir, transform_files=','.join(nut_file_string_filtered))
        

    
    
for i, m, a, s in zip(ID, marker, age, sex):


    print(i,m,a,s)
    transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
    transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
    
    transform_sheet = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_transform_final.xlsx"
    
    filename = f"{i}_{a}_{m}_transform"
    
            
    nut_file_string = nff.list_from_transform_sheet(transform_sheet)


    nff.write_nut_transform_file(filename, r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB\\", transform_input_dir = transform_input_dir, 
                                   transform_output_dir = transform_output_dir, transform_files=','.join(nut_file_string), transform_thumbnail_size = "0.2")















#Checking function


for i, m, a, s in zip(ID, marker, age, sex):
    
    if m == "Calbindin":
        print(i,m,a,s)
        transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_TIF/" #"Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
        transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/temp_output/" #"Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
        transform_thumbs_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/temp_output/thumbnails/" #"Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/thumbnails/" 
        transform_sheet = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_toDo.xlsx"
        
        filename = f"{i}_{a}_{m}_transform"
        
    
        files_in_output = glob(transform_output_dir + "*.tif")
        dict_of_correspondence, orig_name_list, new_name_list = ncf.get_renaming_dict(transform_sheet)
        
        nut_file_string = nff.list_from_transform_sheet(transform_sheet)
        
        nut_file_string_filtered = []
        
        all_tifs_names = []
        
        for file in files_in_output:
            name = (os.path.basename(file)).split(".")[0]
            all_tifs_names.append(name)
        
        for string in nut_file_string:
            name = string.split(",")[0]
            rot = int(string.split(",")[-3])
            scale_x = int(string.split(",")[-2])
            scale_y = int(string.split(",")[-1])
            
            if (rot == 0 and scale_x == 1 and scale_y == 1):
                continue
            else:
                nut_file_string_filtered.append(string)
            
            for i in nut_file_string_filtered:
                name = string.split(",")[0]
                name = f"{name}"
                if name in all_tifs_names:
                    continue
                else:
                    print(name)
        
            
        # ncf.check_files_in_folders(transform_input_dir, transform_output_dir, "tif", "tif")
        # input_file_names, output_file_names = ncf.name_files_in_folders(transform_input_dir, transform_output_dir, "tif", "tif")
        
        # missing_files, missing_files_renamed = ncf.identify_missing_files(input_file_names, output_file_names, dict_of_correspondence)
        
        # if len(missing_files) > 0:
        #     missing_files_df = ncf.create_missing_files_df(missing_files, transform_sheet)
            
        #     nut_string_list = []
        #     for index, row in missing_files_df.iterrows():
        #         nut_string = row["Input file name"] + "," + row["Renamed"] + "," + str(row["Rotation CCW"]) + "," + str(row["Scale X"]) + "," + str(row["Scale Y"])
        #         nut_string_list.append(nut_string)
            
        #     # nff.write_nut_transform_file(filename, r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_files\\", transform_input_dir = transform_input_dir, 
        #     #                               transform_output_dir = transform_output_dir, transform_files=','.join(nut_file_string))
            
        # else:
        #     continue
    else:
        continue












    

    
    