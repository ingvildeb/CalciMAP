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

resourcedir = 'Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_files//'
metadata = resourcedir + "ids_to_make_files_11-05.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]

# Write initial nut transform files:
    
for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
    transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
    transform_sheet = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_transform.xlsx"
    
    filename = f"{i}_{a}_{m}_transform"
    
    nut_file_string = nff.list_from_transform_sheet(transform_sheet)
    
    nff.write_nut_transform_file(filename, r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_files\\", transform_input_dir = transform_input_dir, 
                                  transform_output_dir = transform_output_dir, transform_files=','.join(nut_file_string))
    
    print(nut_file_string)
    
    
    

for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/1_original_tiffs/" 
    transform_output_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
    transform_thumbs_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/thumbnails/" 
    transform_sheet = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/" + i + "_" + a + "_" + m + "_transform.xlsx"
    
    filename = f"{i}_{a}_{m}_transform"
    

    
    dict_of_correspondence, orig_name_list, new_name_list = ncf.get_renaming_dict(transform_sheet)
    ncf.check_files_in_folders(transform_input_dir, transform_output_dir, "tif", "tif")
    input_file_names, output_file_names = ncf.name_files_in_folders(transform_input_dir, transform_output_dir, "tif", "tif")
    
    missing_files, missing_files_renamed = ncf.identify_missing_files(input_file_names, output_file_names, dict_of_correspondence)
    
    if len(missing_files) > 0:
        missing_files_df = ncf.create_missing_files_df(missing_files, transform_sheet)
        
        nut_string_list = []
        for index, row in missing_files_df.iterrows():
            nut_string = row["Input file name"] + "," + row["Renamed"] + "," + str(row["Rotation CCW"]) + "," + str(row["Scale X"]) + "," + str(row["Scale Y"])
            nut_string_list.append(nut_string)
        
        # nff.write_nut_transform_file(filename, r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_files\\", transform_input_dir = transform_input_dir, 
        #                               transform_output_dir = transform_output_dir, transform_files=','.join(nut_file_string))
        
    else:
        continue
    

    
    