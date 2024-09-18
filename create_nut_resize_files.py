# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:51:42 2024

@author: ingvieb
"""

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
    resize_output_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/thumbnails_for_anchoring"
    
    nutil_file_name = f"{i}_{a}_{m}_resizeThumbs"
    nutil_store_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//"
    
    resize_size = 10
    
    nff.write_nut_resize_file(nutil_file_name, nutil_store_path, resize_input_dir = resize_input_dir, resize_output_dir = resize_output_dir, 
                              resize_size=resize_size)

