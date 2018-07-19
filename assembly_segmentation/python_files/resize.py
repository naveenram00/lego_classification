import os, sys
from PIL import Image

def resizes(basewidth):
    img = Image.open('out.png')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save('out.jpg')