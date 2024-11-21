# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 00:05:11 2023

@author: ingvieb
"""


import glob
import shutil
import nutil_scripts.create_nut_file_functions as nff
import nutil_scripts.checking_functions as ncf


nut_file_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_IEB/finalThumbs/"
nut_files = glob.glob(nut_file_path + "*.nut")

data_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/"

done_path = f"{nut_file_path}/done/"

for file in nut_files:
    print(file)
    filename = (file.split(sep="\\")[-1])
    ID = filename.split(sep="_", maxsplit=1)[0]
    stain = (filename.split(sep="_")[2]).split(sep="_f")[0]
    age = filename.split(sep="_")[1]
    
    if stain == "Cresyl":
        stain = "Cresyl_violet"
    else:
        stain = stain

    
    transform_path = f"{data_path}{age}/{stain}/{ID}/2_TIF/"
    thumb_path = f"{data_path}{age}/{stain}/{ID}/thumbnails/"
    
    
    message = ncf.check_files_in_folders(transform_path, thumb_path, ".tif", ".png")
    folder1files, folder2files = ncf.name_files_in_folders(transform_path, thumb_path, ".tif", ".png")
    missing_files = ncf.identify_missing_files(folder1files, folder2files)
    print(len(folder1files), len(folder2files))
    

    
    if len(missing_files) > 0:
        
        nut_string_list = []
        
        for file in missing_files:
            nut_string = file + "," + file + "," + str("0") + "," + str("1") + "," + str("1")
            nut_string_list.append(nut_string)
        
        nff.write_nut_transform_file(f"{ID}_{age}_{stain}_finalThumbs", nut_file_path, name = "", transform_input_dir = transform_path, 
                                     transform_output_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{age}/{stain}/{ID}/",
                                      output_compression = "lzw",  
                                      transform_files = ','.join(nut_string_list), transform_thumbnail_size = "0.2", only_thumbnails = "Yes")
        
        
        
    else:
        shutil.move(file, f"{done_path}{ID}_{age}_{stain}_finalThumbs.nut")