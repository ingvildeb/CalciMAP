# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:07:37 2024

@author: ingvieb
"""



# import required module 
from PIL import Image 
import glob
import os
import re
import json
import pandas as pd


resourcedir = 'Y:/2021_Bjerke_DevMouse_projects/01_DATA//'
metadata = resourcedir + "ids_to_make_files.xlsx"

subjects = pd.read_excel(metadata)    

# ID = subjects["id"]
# age = subjects["age"]


ID = ["mouse111"]
age = ["P35"]

IDDict = dict(zip(ID, age))

basePath = r"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\\"



for ID in IDDict:
    
    age = IDDict.get(ID)
    if age == "P14" or age == "P21":
        template = "template"
    else:
        template = "model"
    

    ID = re.sub("M", "m", ID)
    print(ID,age, template)
    
    filesPath = rf"{basePath}{age}\{ID}\\"
    files = glob.glob(f"{filesPath}*.png")
    
    sliceDicts = []
    
    
    for file in files:
        img = Image.open(file) 
          
        width = img.width 
        height = img.height 
        filename = os.path.basename(file)
        nr = re.findall("[s][0-9][0-9][0-9]", filename)
        
        if len(nr) > 1:
            print("error: more than one potential section number in file name!")
            break
        else:
            nr = nr[0]
            nr = re.sub("[s]", "", nr)
            nr = int(nr)
            print(nr)
    
        sliceDict = {"nr":nr, 
                     "width":width,
                     "height":height,
                     "filename":filename}
        
        sliceDicts.append(sliceDict)

    
    sortedSlicesDicts = sorted(sliceDicts, key=lambda x: (x['nr']))
    
    if age == "P120":
        jsonDict = {"name":f"{ID}_jointAnchoring","target":"ABA_Mouse_CCFv3_2017_25um.cutlas","target-resolution":[428,524,320],"slices":sortedSlicesDicts}

    else:                                            
        jsonDict = {"name":f"{ID}_jointAnchoring","target":f"DeMBAv2_{age}_{template}.cutlas","target-resolution":[570,705,400],"slices":sortedSlicesDicts}
    
    
    with open(rf"{basePath}\{age}\{ID}\{ID}_joint.json", "w") as outfile:
        json.dump(jsonDict, outfile)   

    








    # if os.path.isfile(rf"{basePath}\{age}\{ID}\{ID}_joint.json"):
    #     print(f"Warning: joint JSON file for {ID} {age} already exists")
        
    # else:    
    #     with open(rf"{basePath}\{age}\{ID}\{ID}_joint.json", "w") as outfile:
    #         json.dump(jsonDict, outfile)   
            








