# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:46:01 2023

@author: ingvieb
"""

import os
import pandas as pd
import glob

file_folder = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/P35/Parvalbumin/Mouse815/1_original_tiffs/thumbnails//"
rename_file = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P35\Parvalbumin\Mouse815/Mouse815_P35_Parvalbumin_transform.xlsx"



rename_scheme = pd.read_excel(rename_file)

orig_name = list(rename_scheme["Input file name"])

thumb_name_list = []

for name in orig_name:
    thumb_name = name.split(".tif")[0] + "_thumbnail.png"
    thumb_name_list.append(thumb_name)

new_name = list(rename_scheme["Renamed"])

new_name_list = []

for name in new_name:
    full_name = name + ".png"
    new_name_list.append(full_name)

files = glob.glob(file_folder + "*.png")

dict_of_renaming = dict(zip(thumb_name_list, new_name_list))



def rename_files(directory, file_list, rename_dict):
    
    for key, value in rename_dict.items():
        fullpath = directory + os.sep + key
        outpath = directory + os.sep + value

        if os.path.exists(fullpath):
            #print(key + " will be renamed to " + value)
            os.rename(fullpath,outpath)

            
rename_files(file_folder, files, dict_of_renaming)