# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 08:00:59 2023

@author: ingvieb
"""

import glob
import pandas as pd


resourcedir = r'Y:\2021_Bjerke_DevMouse_projects\03_METADATA//'
metadata = resourcedir + "IDs_to_share_cb-pv.xlsx"

subjects = pd.read_excel(metadata)    

ID = subjects["id"]
marker = subjects["marker"]
age = subjects["age"]
sex = subjects["sex"]

df = pd.DataFrame()
list_of_data = []

for i, m, a, s in zip(ID, marker, age, sex):
    #print(i,m,a,s)

    
    tif_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/{a}/{m}/{i}/2_TIF/" 
    tif_list = glob.glob(f"{tif_dir}*.tif")
    number_of_images = len(tif_list)
    data = pd.DataFrame(data = [i,m,a,s,number_of_images])
    data = data.transpose()
    list_of_data.append(data)
    

concat_df = pd.concat(list_of_data)
concat_df.columns = ["ID", "marker", "age", "sex", "number of tifs"]

stats_df = concat_df.groupby(["marker", "age", "sex"])["number of tifs"].describe()
mean_no_tifs = concat_df.groupby(["marker", "age", "sex"])["number of tifs"].mean()
sum_no_tifs = concat_df.groupby(["marker", "age", "sex"])["number of tifs"].sum()

concat_stats = pd.concat([stats_df, mean_no_tifs, sum_no_tifs], axis=1)
concat_stats.columns = ["count","unique", "top", "freq", "avg number of tifs", "sum number of tifs"]
concat_stats.to_excel(f"{resourcedir}project_stats.xlsx")
concat_df.to_excel(f"{resourcedir}no_tifs_per_mouse.xlsx")