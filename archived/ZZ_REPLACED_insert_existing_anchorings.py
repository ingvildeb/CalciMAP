# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:11:11 2024

@author: ingvieb
"""

import json

ID = "857"
age = "P9"

if age =="P120":
    atlasName = "ABA_Mouse_CCFv3_2017_25um.cutlas"
    targetResolution = [428, 524, 320]
elif age == "P14" or age == "P21":
    atlasName = f"DeMBAv2_{age}_template.cutlas"
    targetResolution = [570,705,400]
else:
    atlasName = f"DeMBAv2_{age}_model.cutlas"
    targetResolution = [570,705,400]


oldAnchoringJson = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\mouse{ID}_jointAnchoring_final_nonlinear.json"
newAnchoringJson = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\Mouse{ID}_jointWithPNN.json"


with open(oldAnchoringJson, 'r') as f:
    oldAnchoringData = json.load(f)
    
with open(newAnchoringJson, 'r') as f:
    newAnchoringData = json.load(f)
    

oldSlicesNumbers = []
oldSlicesAnchoring = []
oldSlicesMarkers = []
oldSlicesWidths = []
oldSlicesHeights = []


for s in oldAnchoringData["slices"]:
    nr = s["nr"]
    anchoring = s["anchoring"]
    markers = s["markers"]
    width = s["width"]
    height = s["height"]
    oldSlicesNumbers.append(nr)
    oldSlicesAnchoring.append(anchoring)
    oldSlicesMarkers.append(markers)
    oldSlicesWidths.append(width)
    oldSlicesHeights.append(height)
    oldAnchorings = dict(zip(oldSlicesNumbers,oldSlicesAnchoring))
    oldMarkers = dict(zip(oldSlicesNumbers,oldSlicesMarkers))
    oldWidths = dict(zip(oldSlicesNumbers,oldSlicesWidths))
    oldHeights = dict(zip(oldSlicesNumbers,oldSlicesHeights))


jsonDict = {"name":f"mouse{ID}_jointAnchoring","target":f"{atlasName}","target-resolution":targetResolution,"slices":[]}

for s in newAnchoringData["slices"]:
    nr = s["nr"]
    width = s["width"]
    height =  s["height"]
    
    oldWidth = oldWidths.get(nr)
    oldHeight =  oldHeights.get(nr)
    filename = s["filename"]
    
    if nr in oldSlicesNumbers:
        anchoring = oldAnchorings.get(nr)
        markers = oldMarkers.get(nr)
        
        newmarkers = []
        for marker_xy in markers:
            xfrom = marker_xy[0]
            yfrom = marker_xy[1]
            xto = marker_xy[2]
            yto = marker_xy[3]
            #print(xfrom, xto)

            xfrom_relative = xfrom/oldWidth
            xto_relative = xto/oldWidth
            yfrom_relative = yfrom/oldHeight
            yto_relative = yto/oldHeight
            #print(xfrom_relative, xto_relative)

            xfrom_new = width*xfrom_relative
            xto_new = width*xto_relative
            yfrom_new = height*yfrom_relative
            yto_new = height*yto_relative
            newmarkers.append([xfrom_new, yfrom_new, xto_new, yto_new])
        
        sliceDict = {"nr":nr, 
                     "width":width,
                     "height":height,
                     "filename":filename,
                     "anchoring":anchoring,
                     "markers":newmarkers}
      

        
    else:
        sliceDict = {"nr":nr, 
                     "width":s["width"],
                     "height":s["height"],
                     "filename":filename}
        
    jsonDict["slices"].append(sliceDict)
    


with open(rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\mouse{ID}_jointAnchoringWithPNN.json", "w") as outfile:
    json.dump(jsonDict, outfile)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    