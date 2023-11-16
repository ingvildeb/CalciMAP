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
    #os.mkdir(fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/2_TIF")

    
    thumbs_input_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/2_TIF/" 
    thumbs_output_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/"
    
    nutil_file_name = f"{i}_{a}_{m}_finalThumbs"
    nutil_store_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\thumbs_files//"
    
    nutilList = nff.nut_list_from_files(thumbs_input_dir)

  
    nff.write_nut_transform_file(nutil_file_name, nutil_store_path, transform_input_dir = thumbs_input_dir, transform_output_dir = thumbs_output_dir, 
                             transform_files = nutilList, only_thumbnails = "Yes", transform_thumbnail_size = "0.1")
    


