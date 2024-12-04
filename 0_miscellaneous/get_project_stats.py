import pandas as pd
import glob

# Reading the metadata
metadata = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA\Animal metadata.xlsx"
read_metadata = pd.read_excel(metadata)

# Reading IDs and filtering by markers
id_file = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//animals_and_stains.xlsx"
markers = ["calbindin", "parvalbumin", "cresyl_violet"]

subjects = pd.read_excel(id_file)
save_dir = r"Y:\2021_Bjerke_DevMouse_projects\03_METADATA//"


for m in markers:
    subjects_filtered = subjects.loc[subjects['marker'] == m]
    ID = subjects_filtered["id"]
    marker = subjects_filtered["marker"]
    age = subjects_filtered["age"]
    sex = subjects_filtered["sex"]

    list_of_data = []
    for i, m, a, s in zip(ID, marker, age, sex):
        tif_dir = fr"Y:/2021_Bjerke_DevMouse_projects/01_DATA/P{a}/{m.capitalize()}/Mouse{i}/2_TIF/" 
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
    concat_stats.to_excel(rf"{save_dir}project_stats_{m}.xlsx")
    concat_df.to_excel(rf"{save_dir}no_tifs_per_mouse_{m}.xlsx")