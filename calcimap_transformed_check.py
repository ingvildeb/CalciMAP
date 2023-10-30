# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 16:27:28 2023

@author: ingvieb
"""


import nutil_scripts.checking_functions as ncf
import nutil_scripts.create_nut_file_functions as nff
from glob import glob
import shutil


nut_file_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_files/"
nut_files = glob(nut_file_path + "*.nut")

data_path = r"Y:/2021_Bjerke_DevMouse_projects/01_DATA/"

done_path = r"Y:/2021_Bjerke_DevMouse_projects/01_DATA/transform_files/done/"


for file in nut_files:
    
    filename = (file.split(sep="\\")[-1])
    ID = filename.split(sep="_", maxsplit=1)[0]
    stain = (filename.split(sep="_", maxsplit=2)[2]).split(sep="_t")[0]
    age = filename.split(sep="_")[1]

    orig_tiff_path = data_path + age + "/" + stain + "/" + ID + "/1_original_tiffs/"
    transform_path = data_path + age + "/" + stain + "/" + ID + "/2_tiffs_rotated_renamed/"
    
    #thumb_path = data_path + age + "/" + stain + "/" + ID + "/2_tiffs_rotated_renamed/thumbnails/"
    
    destination = done_path + filename
    
    
    # read and convert transform file into dict_of_renaming

    print(ID, stain, age)
    
    transformsheet = data_path + age + "/" + stain + "/" + ID + "/" + ID + "_" + age + "_" + stain + "_transform.xlsx"
    dict_of_correspondence, orig_name_list, new_name_list = ncf.get_renaming_dict(transformsheet)
    
    message = ncf.check_files_in_folders(orig_tiff_path, transform_path, ".tif", ".tif")

    folder1files, folder2files = ncf.name_files_in_folders(orig_tiff_path, transform_path, ".tif", ".tif")
      

    missing_files, missing_files_renamed = ncf.identify_missing_files(folder1files, folder2files, dict_of_correspondence)


    if len(missing_files) > 0:
        missing_files_df = ncf.create_missing_files_df(missing_files, transformsheet)
        
        nut_string_list = []
        
        for index, row in missing_files_df.iterrows():
            nut_string = row["Input file name"] + "," + row["Renamed"] + "," + str(row["Rotation CCW"]) + "," + str(row["Scale X"]) + "," + str(row["Scale Y"])
            nut_string_list.append(nut_string)
        
        nff.write_nut_transform_file(ID + "_" + age + "_" + stain + "_transform", nut_file_path, name = ID + "_" + age + "_" + stain, transform_input_dir = orig_tiff_path, transform_output_dir = transform_path,
                                      output_compression = "lzw", transform_files = ','.join(nut_string_list), transform_thumbnail_size = "0.1", only_thumbnails = "No")

        
        
    else:
        shutil.move(file, done_path + ID + "_" + age + "_" + stain + "_transform.nut")