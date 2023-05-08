# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:06:51 2023

@author: ingvieb
"""

import glob
import shutil
import create_nut_file_functions as nff


nut_file_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/thumbs_transform_files/"
nut_files = glob.glob(nut_file_path + "*.nut")

data_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/"

done_path = "Y:/2021_Bjerke_DevMouse_projects/01_DATA/thumbs_transform_files/done//"


for file in nut_files:
    filename = (file.split(sep="\\")[-1])
    ID = filename.split(sep="_", maxsplit=1)[0]
    stain = (filename.split(sep="_", maxsplit=2)[2]).split(sep="_t")[0]
    age = filename.split(sep="_")[1]

    orig_tiff_path = data_path + age + "/" + stain + "/" + ID + "/2_tiffs_rotated_renamed/"
    thumb_path = orig_tiff_path + "new_thumbs/thumbnails/"
    
    destination = done_path + filename

    orig_tiffs = glob.glob(orig_tiff_path + "*.tif")
    orig_tiffs_no = len(orig_tiffs)
    
    existing_thumbs = glob.glob(thumb_path + "*.png")
    existing_thumbs_no = len(existing_thumbs)
    
    if orig_tiffs_no == existing_thumbs_no:
        #print(ID + " : done")
        shutil.move(file, destination)
        print(f"moving \n {file} \n to \n {destination}")
        
    else:
        print(ID + " : not done")
    
    print(orig_tiffs_no, existing_thumbs_no)

    thumblist = []
    
    for thumb in existing_thumbs:
        name = (thumb.split(sep="\\")[1]).split(sep="_thumbnail")[0]
        thumblist.append(name)        
        
    tiflist = []
    
    for tif in orig_tiffs:
        name = (tif.split(sep="\\")[1]).split(sep=".tif")[0]
        tiflist.append(name)        
    
    remaining_thumbs = []
    
    for tif in tiflist:
        if tif in thumblist:
            continue
        else:
            remaining_thumbs.append(tif + ".tif" + "," + tif + ".tif" +  ",0,1,1")
    
    if len(remaining_thumbs) > 0:                
            
        nff.write_nut_transform_file(ID + "_" + age + "_" + stain + "_thumbs", "Y:/2021_Bjerke_DevMouse_projects/01_DATA/thumbs_transform_files/",
                                     transform_input_dir = orig_tiff_path,
                                     transform_output_dir = orig_tiff_path + "new_thumbs/",
                                     transform_files = ', '.join(remaining_thumbs),
                                     only_thumbnails = "Yes",
                                     transform_thumbnail_size = "0.01")