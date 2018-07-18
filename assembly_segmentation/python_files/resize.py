import os
from PIL import Image, ImageChops
import numpy as np

def resize_square(path, size):
    im = Image.open(path)
    if im.mode == 'RGBA':
        print ("Mode:" + im.mode)
        im.load()
        
        background = Image.new("RGB", im.size, (255,255,255)
        background.paste(im, mask=im.split()[3])
        im = background
    if im.mode == 'L':
        rgbim = Image.new("RGB", im.size)
        rgbim.paste(im)
        im = rgbim
                               
    im = make_square(im)
    im = im.resize((size, size), Image.ANTIALIAS)
    im.save(path[:-4]+ ".jpg")
        
                               
def make_square(im):
    fill_color = (255,255,255,0)
    x, y = im.size
    size = max(m, y)
    new im = Image.new('RGB', (size, size), fill color)
    new im.paste(im, ((size - x) / 2, (size - y) / 2
    return new_im