import os
import glob
import re
import pandas as pd


# Path to Excel sheet listing all animal IDs with metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"

# Read and filter Excel sheet to the selected IDs and markers
subjects = pd.read_excel(metadata)    
markers = ["cresyl_violet", "calbindin", "parvalbumin"]
ages = [9,14,21,35,120]
subjects_filtered = subjects.loc[(subjects['age'].isin(ages)) & (subjects['marker'].isin(markers))] 

# Listing the metadata variables from the Excel sheet that are going to be used in our folder names
ID = subjects_filtered["id"]
marker = subjects_filtered["marker"]
age = subjects_filtered["age"]
sex = subjects_filtered["sex"]

marker_shortnames = {"parvalbumin":"parv", "calbindin":"calb", "cresyl_violet":"CV"}

# Checking that all CZI files adheres to the file naming convention

for i,m,a,s in zip(ID,marker,age,sex):
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    CZI_path = rf"{file_base_path}1_CZI\\"
    CZI_files = glob.glob(f"{CZI_path}*.czi")

    regex_pattern = fr"^mouse{i}_P{a}_{s}_{marker_shortnames[m]}_(\d{{3}}(_\d{{3}})*)\.czi$"
    #print(CZI_path)
    for file in CZI_files:
        name = os.path.basename(file)

        if re.match(regex_pattern, name):
            continue
        else:
            print(f"{name} does NOT match the expected format.")
    print("--------------------")


# Checking that all tiffs files adheres to the file naming convention

for i,m,a,s in zip(ID,marker,age,sex):
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    TIF_path = rf"{file_base_path}2_TIF\\"
    TIF_files = glob.glob(f"{TIF_path}*")

    regex_pattern = fr"^mouse{i}_P{a}_{s}_{marker_shortnames[m]}_s\d{{3}}\.tif$"

    print(TIF_path)
    for file in TIF_files:
        name = os.path.basename(file)

        if re.match(regex_pattern, name):
            continue
        else:
            print(f"{name} does NOT match the expected format.")
    print("--------------------")


# Check that no excess files beyond the expected ones exist
def normalize_path(path):
    # Normalize paths by removing trailing slashes and converting to lower case
    return os.path.normpath(path).lower()

def check_folder_contents(folder_path, expected_extension, allow_one_json=False):
    # List all files in the folder
    files = glob.glob(f"{folder_path}*")
    unexpected_files = []
    json_files_count = 0

    for file in files:
        # Normalize path and get file extension
        normalized_path = normalize_path(file)
        file_extension = os.path.splitext(normalized_path)[1].lower()
        
        # Check for JSON files if allowed
        if allow_one_json and file_extension == ".json":
            json_files_count += 1
            continue
        
        # Check if the file has the expected extension
        if file_extension != expected_extension:
            unexpected_files.append(os.path.basename(file))

    # Check if there's exactly one JSON file if required
    if allow_one_json and json_files_count != 1:
        unexpected_files.append(f"Expected exactly one json file, found {json_files_count}.")

    return unexpected_files

for i, m, a, s in zip(ID, marker, age, sex):
    file_base_path = rf"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/"
    CZI_path = rf"{file_base_path}1_CZI/"
    TIF_path = rf"{file_base_path}2_TIF/"
    thumbs_path = rf"{file_base_path}thumbnails/"
    anchoring_path = rf"{file_base_path}thumbnails_for_anchoring/"

    expected_content_parent = {
        normalize_path(CZI_path), 
        normalize_path(TIF_path), 
        normalize_path(thumbs_path), 
        normalize_path(anchoring_path)
    }
    
    actual_content_parent = set(normalize_path(path) for path in glob.glob(f"{file_base_path}*"))

    print(f"\nChecking Mouse{i} P{a} {m}")

    unexpected_files = actual_content_parent - expected_content_parent
    if unexpected_files:
        for content in unexpected_files:
            print(f"NB! Unexpected file {os.path.basename(content)} found. Please check.")
    else:
        print("Directory is well organized.")

    # Check contents of each folder
    folder_checks = [
        (CZI_path, ".czi", False),
        (TIF_path, ".tif", False),
        (thumbs_path, ".png", False),
        (anchoring_path, ".png", True)
    ]

    for folder_path, extension, allow_one_json in folder_checks:
        normalized_folder_path = normalize_path(folder_path)
        if normalized_folder_path in actual_content_parent:
            unexpected_files = check_folder_contents(folder_path, extension, allow_one_json)
            if unexpected_files:
                for file in unexpected_files:
                    print(f"NB! Unexpected file {file} in {folder_path}. Please check.")
        else:
            print(f"NB! Expected folder {folder_path} is missing. Please check.")




# Check that the same files exist in tif and thumbnail paths
## Check this again after all series are done.


for i,m,a,s in zip(ID,marker,age,sex):
    file_base_path = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\P{a}\{m.capitalize()}\Mouse{i}\\"
    TIF_path = rf"{file_base_path}2_TIF\\"
    thumbnail_path = rf"{file_base_path}thumbnails\\"
    anchoring_thumbnail_path = rf"{file_base_path}thumbnails_for_anchoring\\"

    TIF_files = glob.glob(rf"{TIF_path}*.tif")
    thumbnails = glob.glob(rf"{thumbnail_path}*.png")
    anchoring_thumbnails = glob.glob(rf"{anchoring_thumbnail_path}*.png")

    

    if len(TIF_files) == len(thumbnails) == len(anchoring_thumbnails):
        #print("All folders have the same number of files")
        continue

    else:
        print(f"File number mismatch for Mouse{i} P{a} {m}")
        print(f"TIF_files: {len(TIF_files)}, thumbnails: {len(thumbnails)}, anchoring_thumbnails: {len(anchoring_thumbnails)}")
        #break