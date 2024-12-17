import os

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def bytes_to_tb(bytes):
    tb_size = bytes / 1099511627776
    return tb_size

def get_tb_size(dir_list = []):
    total_dir_size = 0
    for dir in dir_list:
        dir_size = get_dir_size(dir)
        dir_size_tb = bytes_to_tb(dir_size)
        total_dir_size = total_dir_size + dir_size_tb
    return total_dir_size

dev_ages = [9,14,21,35]
file_base_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\\"

calb_dev_paths = []
parv_dev_paths = []
calb_adult_paths = [r'Y:\\2021_Bjerke_DevMouse_projects\\01_DATA\\\\P120\\Calbindin\\\\']
parv_adult_paths = [r'Y:\\2021_Bjerke_DevMouse_projects\\01_DATA\\\\P120\\Parvalbumin\\\\',
                    r'Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\Mouse\Parvalbumin\\',
                    r'Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\Mouse\Nissl\\']
cv_paths = [r'Y:\\2021_Bjerke_DevMouse_projects\\01_DATA\\\\P120\\Cresyl_violet\\\\']
parv_rat_paths = [r'Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\Rat\Nissl',
                  r'Y:\NESYS_Active_projects\2019_Laja_Brainwide_Parvalbumin\Rat\Parvalbumin']

for age in dev_ages:
    calb_path = rf"{file_base_path}P{age}\Calbindin\\"
    calb_dev_paths.append(calb_path)

    parv_path = rf"{file_base_path}P{age}\Parvalbumin\\"
    parv_dev_paths.append(parv_path)

    cv_path = rf"{file_base_path}P{age}\Cresyl_violet\\"
    cv_paths.append(cv_path)


calb_dev_size = get_tb_size(calb_dev_paths)
parv_dev_size = get_tb_size(parv_dev_paths)
calb_adult_size = get_tb_size(calb_adult_paths)
parv_adult_size = get_tb_size(parv_adult_paths)
cv_size = get_tb_size(cv_paths)
parv_rat_size = get_tb_size(parv_rat_paths)

print(f"Calbindin developmental mouse data size: {calb_dev_size}")
print(f"Parvalbumin developmental mouse data size: {parv_dev_size}")
print(f"Calbindin adult mouse data size: {calb_adult_size}")
print(f"Parvalbumin adult mouse data size: {parv_adult_size}")
print(f"Cresyl violet (neuron distributions) mouse data size: {cv_size}")
print(f"Parvalbumin adult rat data size: {parv_rat_size}")
