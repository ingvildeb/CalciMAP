# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:09:02 2023

@author: ingvieb
"""

import pandas as pd


metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\Animal metadata.xlsx"
readMeta = pd.read_excel(metadata)

id_file = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\IDs_to_share_cb-pv.xlsx"

readIDs = pd.read_excel(id_file)
sharedIDs_list = list(readIDs["ID"])

readMeta_indexed = readMeta.set_index("ID")
readMeta_selected = readMeta_indexed.loc[sharedIDs_list]

readMeta_selected.to_excel(r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\SelectedMetadata.xlsx")