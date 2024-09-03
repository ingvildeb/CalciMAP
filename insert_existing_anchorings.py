# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:11:11 2024

@author: ingvieb
"""

import json

ID = "311"
age = "P21"



oldAnchoringJson = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\mouse{ID}_finalWithCorr.json"
newAnchoringJson = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\1_joint_for_quicknii\mouse{ID}_joint.json"





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


jsonDict = {"name":"mouse{ID}_jointAnchoring","target":"DeMBA_P21_template.cutlas","target-resolution":[570,705,400],"slices":[]}

for s in newAnchoringData["slices"]:
    nr = s["nr"]
    width = oldWidths.get(nr)
    height =  oldHeights.get(nr)
    filename = s["filename"]
    
    if nr in oldSlicesNumbers:
        anchoring = oldAnchorings.get(nr)
        markers = oldMarkers.get(nr)
        sliceDict = {"nr":nr, 
                     "width":width,
                     "height":height,
                     "filename":filename,
                     "anchoring":anchoring,
                     "markers":markers}
        
    else:
        sliceDict = {"nr":nr, 
                     "width":s["width"],
                     "height":s["height"],
                     "filename":filename}
        
    jsonDict["slices"].append(sliceDict)
    

with open(rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\{age}\Mouse{ID}\resize_test_25\mouse{ID}_jointAnchoring.json", "w") as outfile:
    json.dump(jsonDict, outfile)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    