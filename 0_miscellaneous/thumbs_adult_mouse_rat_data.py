import sys
import os
import pandas as pd

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import create_nut_file_functions as nff

# List the IDs and markers with files to be renamed
ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25207:"Rat",25208:"Rat"}
markers = ["parvalbumin", "nissl"]

for m in markers:
    for i in ids_species:
        species = ids_species.get(i)

        
        file_base_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\{species}{i}\\"
        print(file_base_path)
        transform_input_dir = fr"{file_base_path}2_TIF/"
        nut_file_string = nff.nut_list_from_files(transform_input_dir)

    
        nff.write_nut_transform_file(f"{species}{i}_{m.capitalize()}_finalThumbs", 
                                    r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\transform_IEB\0369//", 
                                    transform_input_dir = transform_input_dir, 
                                    transform_output_dir = file_base_path, 
                                    transform_files = nut_file_string, 
                                    only_thumbnails = "Yes", 
                                    transform_thumbnail_size = "0.2")