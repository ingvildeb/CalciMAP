import sys
import os
import pandas as pd
import glob
import shutil

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import nutil_checker_functions as ncf


### Example usage
# Provide a directory that contains all the nut files to be checked
    
nut_file_directory = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB//"

# Check transform files (thumbnails only or not)

files = glob.glob(rf"{nut_file_directory}/*.nut")
done_path = f"{nut_file_directory}done//"

check_only = True

for file in files:    
    print(f"Checking {os.path.basename(file)}")
    _, _, _, only_thumbnails = ncf.read_nut_transform_file(file)
    name = os.path.basename(file)

    
    if only_thumbnails == "Yes":
        missing_files = ncf.check_nut_file(file) 
        print(f"{len(missing_files)} files missing")

        if check_only == False:
            if len(missing_files) > 0:
                nut_string = ncf.missing_files_to_string(missing_files)
                ncf.change_nut_file_files(file, f"transform_files = {nut_string}")
                
            else:
                shutil.move(file, f"{done_path}{name}")
        else:
            continue

    if only_thumbnails == "No":
        missing_files, missing_thumbs = ncf.check_nut_file(file) 
        print(f"{len(missing_files)} tiffs missing")
        print(f"{len(missing_thumbs)} thumbnails missing")
        
        if check_only == False:

            if len(missing_thumbs) > 0:
                nut_string = ncf.missing_files_to_string(missing_thumbs)
                ncf.change_nut_file_files(file, f"transform_files = {nut_string}")
                
            else:
                shutil.move(file, f"{done_path}{name}")
        else:
            continue
    