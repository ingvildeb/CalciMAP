import pandas as pd

# Reading the metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\Animal metadata.xlsx"
read_metadata = pd.read_excel(metadata)

# Reading IDs and filtering by markers
id_file = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"
markers = ["calbindin", "parvalbumin", "cresyl_violet"]

subjects = pd.read_excel(id_file)


subjects_filtered = subjects.loc[subjects['marker'].isin(markers)]
sharedIDs_list = list(subjects_filtered["id"])
sharedIDs_list = list(set(sharedIDs_list))


perfusion_notes = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\Perfusion_metadata.xlsx"
read_perfusion_notes = pd.read_excel(perfusion_notes)

perfusion_notes_indexed = read_perfusion_notes.set_index("ID")
perfusion_notes_selected = perfusion_notes_indexed.loc[sharedIDs_list]
perfusion_notes_selected = perfusion_notes_selected.reset_index()

perfusion_notes_selected.to_excel(rf"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\CALCIMAP_Data descriptor\Supplementary_data\S1_Perfusion notes.xlsx", index=False)