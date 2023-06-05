# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:52:19 2023

@author: ingvieb
"""

import pandas as pd
import create_nut_file_functions as nff
from glob import glob


resourcedir = 'Y:/2021_Bjerke_DevMouse_projects/01_DATA/thumbs_transform_files//'
metadata = resourcedir + "ids_to_make_files.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]

# Write files to extract cells:
    
for i, m, a, s in zip(ID, marker, age, sex):
    print(i,m,a,s)
    transform_input_dir = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/" + a + "/" + m + "/" + i + "/2_tiffs_rotated_renamed/" 
    transformfiles = glob(transform_input_dir + "*.tif")

    file_list = []
    for f in transformfiles:
        file = f.split("\\")[-1]
        file_in_nut = file + "," + file + ",0,1,1"
        file_list.append(file_in_nut)
    

   
    nff.write_nut_transform_file(i + "_" + a + "_" + m + "_thumbs", "Y:/2021_Bjerke_DevMouse_projects/01_DATA/thumbs_transform_files/",
                                 transform_input_dir = transform_input_dir,
                                 transform_output_dir = transform_input_dir + "new_thumbs/",
                                 transform_files = ', '.join(file_list),
                                 only_thumbnails = "Yes",
                                 transform_thumbnail_size = "0.02")
    


