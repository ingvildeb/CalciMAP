import glob
import os
import re
import sys

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import file_naming_functions as fnf

# List the IDs and markers with files to be renamed
ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25203:"Rat",25204:"Rat"}
markers_startnr = {"parvalbumin":3, "nissl":1}

markers = ["parvalbumin"]
ids = [25206]

check_only = True

for m in markers:
    for i in ids:
        species = ids_species.get(i)
        startnr = markers_startnr.get(m)

        file_base_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\{species}{i}\\"
        tiff_dir = rf"{file_base_path}2_TIF\\"
        thumbs_dir = rf"{file_base_path}thumbnails\\"
        anchoring_dir = rf"{file_base_path}thumbnails_for_anchoring\\"
        anchoring_working_dir = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{species}{i}\\"
        
        dirs = [tiff_dir, thumbs_dir, anchoring_dir, anchoring_working_dir]
        dirs_extension = {tiff_dir: ".tif", thumbs_dir: "_thumbnail.png", 
                          anchoring_dir: "_thumbnail.png", anchoring_working_dir: "_thumbnail.png"}
        dirs_json = {tiff_dir: None, thumbs_dir: None, 
                          anchoring_dir: None, 
                          anchoring_working_dir: rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{species}{i}\{species}{i}_{m}_Anchoring.json"}

        for dir in dirs:
            extension = dirs_extension.get(dir)
            print(f"{dir}") 
            print(len(glob.glob(f"{dir}*{extension}")))
            renumber_dict = fnf.sequential_to_real_sections(dir,startnr,3,extension)
            json_file = dirs_json.get(dir)
        
            if check_only == True:
                print(renumber_dict)
                if json_file:
                    print(f"Looking for {json_file}")
                    if os.path.exists(json_file):
                        print("The JSON file exists.")
                    else:
                        print("The JSON file does not exist.")
            else:
                print(f"Renumbering {dir}...")
                fnf.exchange_sequential_sections(dir,renumber_dict,json_file,extension)


