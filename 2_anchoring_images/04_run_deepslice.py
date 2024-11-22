
from DeepSlice import DSModel     
import json

species = 'mouse' #available species are 'mouse' and 'rat'

Model = DSModel(species)

ID = "6"
blocks = ["block1", "block2"]


for block in blocks:
    folderpath = rf'Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P120\{ID}\for_deepslice/{block}//'
    
    #here you run the model on your folder
    #try with and without ensemble to find the model which best works for you
    #if you have section numbers included in the filename as _sXXX specify this :)
    Model.predict(folderpath, ensemble=True, section_numbers=True)    
    
    #If you would like to normalise the angles (you should)
    Model.propagate_angles()                     

    #To reorder your sections according to the section numbers 
    Model.enforce_index_order()    

    #alternatively if you know the precise spacing (ie; 1, 2, 4, indicates that section 3 has been left out of the series) Then you can use      
    #Furthermore if you know the exact section thickness in microns this can be included instead of None
    #if your sections are numbered rostral to caudal you will need to specify a negative section_thickness      
    Model.enforce_index_spacing(section_thickness = -40)
    
    #now we save which will produce a json file which can be placed in the same directory as your images and then opened with QuickNII. 
    Model.save_predictions(folderpath + f'{block}_ds')
    
 
    
jsonDict = {"name":f"{ID}_jointAnchoring_ds","target":"ABA_Mouse_CCFv3_2017_25um.cutlas","target-resolution":[428, 524, 320],"slices":[]}


for block in blocks:
    dsAnchoringJson = rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P120\Mouse{ID}\for_deepslice/{block}/{block}_ds.json"
    
    
    with open(dsAnchoringJson, 'r') as f:
        dsAnchoringJson = json.load(f)
    
    slices = dsAnchoringJson["slices"]
    jsonDict["slices"].extend(slices)

    
with open(rf"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\P120\Mouse{ID}\mouse{ID}_jointAnchoring_ds.json", "w") as outfile:
    json.dump(jsonDict, outfile)   