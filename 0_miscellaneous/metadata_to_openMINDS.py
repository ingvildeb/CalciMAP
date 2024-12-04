# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:09:02 2023

@author: ingvieb
"""
import pandas as pd

# Reading the metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\Animal metadata.xlsx"
read_metadata = pd.read_excel(metadata)

# Reading IDs and filtering by markers
id_file = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"
markers = ["calbindin", "parvalbumin", "cresyl_violet"]

subjects = pd.read_excel(id_file)


for marker in markers:
    subjects_filtered = subjects.loc[subjects['marker'] == marker] 
    print(f"{marker}: {len(subjects_filtered)}")
    sharedIDs_list = list(subjects_filtered["id"])

    # Selecting and processing the metadata
    read_metadata_indexed = read_metadata.set_index("ID")
    read_metadata_selected = read_metadata_indexed.loc[sharedIDs_list]
    read_metadata_selected = read_metadata_selected.reset_index()

    selected_metadata = read_metadata_selected[["ID", "Sex", "Age group", "Age \n(in days)", "Weight (g)"]]
    selected_metadata.columns = ['Subject/Tissue/Sample Group ID', 'Biological sex', 'Age category', 'Age', 'Weight']

    # Add prefix and replace values as needed
    selected_metadata['Subject/Tissue/Sample Group ID'] = 'Mouse' + selected_metadata['Subject/Tissue/Sample Group ID'].astype(str)
    selected_metadata['Age'] = 'Postnatal day ' + selected_metadata['Age'].astype(str)
    selected_metadata['Biological sex'] = selected_metadata['Biological sex'].replace({'M': 'Male', 'F': 'Female'})
    selected_metadata['Age category'] = selected_metadata['Age category'].replace({35: 'adolescent', 21: 'juvenile', 17: 'juvenile', 14: 'juvenile', 9: 'juvenile', 'Adult': 'adult'})

    # Create the new columns with the default values
    default_values = {
        'Strain': 'C57BL_6',
        'Species': 'Mus musculus',
        'Handedness': 'None',
        'Laterality (tissue)': 'None',
        'Pathology': 'None',
        'Phenotype': 'wildtype',
        'Origin (tissue)': 'brain',
        'Sampletype (tissue)': 'tissue slice',
        'Brain area': 'Whole brain'
    }

    # Adding default columns to the selected metadata
    for col, val in default_values.items():
        selected_metadata[col] = val

    # Reorder the columns
    new_columns = [
        'Subject/Tissue/Sample Group ID',  # already set above
        'Biological sex',
        'Age category',
        'Species',  # to be added with default value 'Mouse'
        'Age',
        'Weight',
        'Strain',
        'Pathology',
        'Phenotype',
        'Handedness',
        'Laterality (tissue)',
        'Origin (tissue)',
        'Sampletype (tissue)',
        'Brain area'
    ]


    # Reorder selected_metadata
    final_df = selected_metadata[new_columns]


    # Filter DataFrames based on "Age category"
    adult_df = final_df[final_df['Age category'] == 'adult']
    rest_df = final_df[final_df['Age category'] != 'adult']

    # Save the DataFrames to Excel files
    adult_df.to_excel(rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\EBRAINS_data_sharing\openminds_metadata\adult_data_{marker}.xlsx", index=False)
    rest_df.to_excel(rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\EBRAINS_data_sharing\openminds_metadata\dev_data_{marker}.xlsx", index=False)

