import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff

# List the IDs and markers with files to be renamed
#ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25203:"Rat",25204:"Rat"}
ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25203:"Rat",25204:"Rat"}
markers = ["parvalbumin", "nissl"]

for m in markers:
    for i in ids_species:
        species = ids_species.get(i)

        
        file_base_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\{species}{i}\\"
        print(file_base_path)
        transform_input_dir = fr"{file_base_path}2_TIF/"
        nut_file_string = nff.nut_list_from_files(transform_input_dir)

    
        nff.write_nut_transform_file(f"{species}{i}_{m.capitalize()}_finalThumbs", 
                                    r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//", 
                                    transform_input_dir = transform_input_dir, 
                                    transform_output_dir = file_base_path, 
                                    transform_files = nut_file_string, 
                                    only_thumbnails = "Yes", 
                                    transform_thumbnail_size = "0.2")
        

for m in markers:
    for i in ids_species:
        species = ids_species.get(i)
        file_base_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\{species}{i}\\"
        os.mkdir(fr"{file_base_path}/thumbnails_for_anchoring")
    
        nff.write_nut_resize_file(filename = f"{species}{i}_{m.capitalize()}_resizeThumbs", 
                              storepath = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//", 
                              resize_input_dir = fr"{file_base_path}thumbnails/", 
                              resize_output_dir = fr"{file_base_path}thumbnails_for_anchoring/", 
                              resize_size = 10)
        

nut_file_directory = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//"
files = glob.glob(rf"{nut_file_directory}/*.nut")

# Check resize files
       
for file in files:
    print(f"Checking {os.path.basename(file)}")
    message, len_input_files, len_output_files = ncf.check_nut_resize_file(file, "png")
    print(message, f"{len_output_files} out of {len_input_files} done")

    

# Copy all resized files to anchoring location

for m in markers:
    for i in ids_species:
        species = ids_species.get(i)
        file_base_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\{species}{i}\\"
        thumbs_path = fr"{file_base_path}/thumbnails_for_anchoring//"
        anchoring_path = fr"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{i}\\"
        
        all_thumbs = glob.glob(thumbs_path + "*.png")
        
        if os.path.exists(anchoring_path):

            for thumb in all_thumbs:
                name = os.path.basename(thumb)
                shutil.copy(thumb, f"{anchoring_path}{name}")

        else:
            os.mkdir(anchoring_path)
            anchoring_path = fr"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P{a}\Mouse{i}\\"

            for thumb in all_thumbs:
                name = os.path.basename(thumb)
                shutil.copy(thumb, f"{anchoring_path}{name}")