# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 11:05:38 2024

@author: ingvieb
"""


# Importing Image class from PIL module 
from PIL import Image 
Image.MAX_IMAGE_PIXELS = None

# Opens a image in RGB mode 
im = Image.open(r"C:\Users\ingvieb\mouse192_P35_M_CV_s142.tif") 


half = 0.5
out = im.resize( [int(half * s) for s in im.size] )

im.save(r'C:\Users\ingvieb\mouse192_P35_M_CV_s142.png')