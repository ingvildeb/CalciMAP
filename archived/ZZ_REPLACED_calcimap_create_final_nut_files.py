# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 19:09:05 2023

@author: ingvieb
"""


import pandas as pd
import nutil_scripts.create_nut_file_functions as nff
from glob import glob
import re
import os

resourcedir = r'Y:\2021_Bjerke_DevMouse_projects\03_METADATA//'
metadata = resourcedir + "IDs_to_share_cb-pv.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]


for i, m, a, s in zip(ID, marker, age, sex):
    #print(i,m,a,s)
    os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/2_TIF")

    
    transform_input_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/2_tiffs_rotated_renamed/" 
    transform_output_dir = fr"{transform_input_dir}temp_nutil_output"
    
    nutil_file_name = f"{i}_{a}_{m}_finalNutil"
    nutil_store_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_files//"
    
    finalNutil_file = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/{i}_{a}_{m}_finalNutil.xlsx"
    
    if os.path.exists(finalNutil_file):
    
        transform_files = nff.list_from_transform_sheet(finalNutil_file)    
        nff.write_nut_transform_file(nutil_file_name, nutil_store_path, transform_input_dir = transform_input_dir, transform_output_dir = transform_output_dir, 
                                 transform_files = ','.join(transform_files), only_thumbnails = "No", transform_thumbnail_size = "0.1")
    else:
        continue
    
