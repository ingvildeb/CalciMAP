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
ids = [81265]

check_only = True

for m in markers:
    for i in ids:
        species = ids_species.get(i)
        tiff_dir = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{m.capitalize()}\Mouse{i}\2_TIF\\"

        renumber_dict = fnf.sequential_to_real_sections(tiff_dir,3,3)
        
        if check_only == True:
            print(renumber_dict)
        else:
            continue
            #fnf.exchange_sequential_sections(tiff_dir,renumber_dict)


