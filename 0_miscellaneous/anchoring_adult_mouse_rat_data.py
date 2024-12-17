import glob
import os
import re
import sys
import json
import shutil

# Import from module in parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
brain_section_scripts_path = os.path.join(parent_dir, 'brain_section_scripts')
sys.path.insert(0, brain_section_scripts_path)

import alignment_json_utils as aju

# List the IDs and markers with files to be renamed
ids_species = {81264:"Mouse",81265:"Mouse",81266:"Mouse",81267:"Mouse",25205:"Rat",25206:"Rat",25203:"Rat",25204:"Rat"}
species_target = {"Mouse": "ABA_Mouse_CCFv3_2017_25um.cutlas", "Rat": "WHS_Rat_v4_39um.cutlas"}
species_resolution = {"Mouse": [428,524,320], "Rat": [512.0, 1024.0, 512.0]}
species_suffix = {"Mouse": "nonlin", "Rat": "WHSv4_nonlinear"}
markers = ["parvalbumin"]
ids = [25203, 25204, 25205, 25206, 81264, 81265, 81266, 81267]

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

# Create anchoring files with nissl & pv

for i in ids:
        species = ids_species.get(i)
        print(f"Preparing file for {species}{i}")
        anchoring_dir = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{species}{i}\\"
        target = species_target.get(species)
        target_resolution = species_resolution.get(species)

        aju.create_quicknii_slicedict(anchoring_dir, 
                        rf"{anchoring_dir}{species}{i}_joint",
                        rf"{species}{i}_joint",
                        target,
                        target_resolution)   
        
        aju.insert_existing_anchorings(rf"{anchoring_dir}{species}{i}_parvalbumin_Anchoring.json", 
                                rf"{anchoring_dir}{species}{i}_joint.json", 
                                rf"{anchoring_dir}{species}{i}_jointAnchoring",
                                f"{species}{i}_Anchoring", 
                                target, 
                                target_resolution,
                                True)
        

# Split jsons into nissl & parv separate files


specific_strings = ["parv", "nissl"]
string_markers = {"parv": "Parvalbumin", "nissl": "Nissl"}

for i in ids:
    species = ids_species.get(i)
    anchoring_dir = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\Anchoring_workspace\{species}{i}\\"
    target = species_target.get(species)
    json_file = rf"{anchoring_dir}{species}{i}_jointAnchoring_final_nonlinear.json"
    json_data = aju.read_json(json_file)

    for str in specific_strings:
        marker = string_markers.get(str)
        specific_dict = aju.split_json(json_data, str)
        specific_json = aju.create_quicknii_json_dict(json_data["name"], target, json_data["target-resolution"])
        specific_json["slices"] = specific_dict
        final_anchoring_path = rf"Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\{species}\{marker}\{species}{i}\thumbnails_for_anchoring\\"
        
        with open(rf"{anchoring_dir}{species}{i}_anchoring_{str}.json", "w") as outfile:
            json.dump(specific_json, outfile)  

        with open(f"{final_anchoring_path}{species}{i}_anchoring_{str}.json", "w") as outfile:
            json.dump(specific_json, outfile)
