

import os

from PIL import Image
import numpy as np


im = Image.open("/usr/src/lego_classification/part_recognition/lego_images/train/4/part5-4680.jpg") #Opening image
im = im.resize((32, 32), Image.ANTIALIAS)

print im.mode


rgbim = Image.new("RGB", im.size)
rgbim.paste(im)

im = rgbim

print im.mode

im = (np.array(im))
print im
r = im[:,:,0] #Slicing to get R data
g = im[:,:,1] #Slicing to get G data
b = im[:,:,2] #Slicing to get B data