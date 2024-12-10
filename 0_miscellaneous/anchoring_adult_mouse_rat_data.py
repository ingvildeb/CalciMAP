import glob
import os
import re
import sys

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import alignment_json_utils as aju

# List the IDs and markers with files to be renamed
ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25203:"Rat",25204:"Rat"}
markers_startnr = {"parvalbumin":3, "nissl":1}
species_target = {"Mouse": "ABA_Mouse_CCFv3_2017_25um.cutlas", "Rat": "WHS_Rat_v4_02_39um.cutlas"}
species_resolution = {"Mouse": [428,524,320], "Rat": [512.0, 1024.0, 512.0]}
species_suffix = {"Mouse": "nonlin", "Rat": "WHSv4_nonlinear"}
markers = ["parvalbumin"]
ids = [81265, 81266, 81267]

check_only = True

for m in markers:
    for i in ids:
        species = ids_species.get(i)
        anchoring_dir = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{species}{i}\\"
        target = species_target.get(species)
        target_resolution = species_resolution.get(species)
        suffix = species_suffix.get(species)

        print(anchoring_dir)
        print(target)
        print(target_resolution)
        aju.create_quicknii_slicedict(anchoring_dir, 
                                rf"{anchoring_dir}{species}{i}_{m}_newAnchoring",
                                rf"{species}{i}_{m}_newAnchoring",
                                target,
                                target_resolution)   
        
        aju.insert_existing_anchorings(rf"{anchoring_dir}{i}_{suffix}.json", 
                                    rf"{anchoring_dir}{species}{i}_{m}_newAnchoring.json", 
                                    rf"{anchoring_dir}{species}{i}_{m}_Anchoring",
                                    f"{species}{i}_{m}_Anchoring", 
                                    target, 
                                    target_resolution,
                                    False)
