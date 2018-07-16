"""
This file contains tools to use in order to convert one or multiple 
image files into a numpy array which is in the cifar10 format style.

This assumes the following:

10 classes of images in folders titles simple 0 - 9 like so:

.../input dir
				/0
					images of class 0
				/1
					images of class 1
				etc
"""
import os

from PIL import Image
import numpy as np


#Directory containing images you wish to convert
input_dir = "/usr/src/lego_classification/part_recognition/lego_images/60"

def resize_and_format (im):
	#creates a 32 by 32 rgb jpg version of the image

	im = im.resize((32, 32), Image.ANTIALIAS)
				
	if im.mode != 'RGB':
		print("Mode:" + im.mode)
		#im = im.convert('RBG')
		#im.save(image.toString() + ".jpg")
		
		im.load() # required for png.split()

		background = Image.new("RGB", im.size, (255, 255, 255))
		background.paste(im, mask=im.split()[3]) # 3 is the alpha channel

		background.save(image + '.jpg', 'JPEG', quality=80)
		im = background
	return im

def numpy_arr(im):
	im = (np.array(im))

	r = im[:,:,0].flatten()
	g = im[:,:,1].flatten()
	b = im[:,:,2].flatten()

	out = np.array(list(r) + list(g) + list(b),np.uint8)
	return out

def cifar_byte(im, label):
	#creates a numpy array version of the image (in the style of cifar10)
	
	label = [label]

	out = np.array(list(label) + list(numpy_arr(im)))
	return out

	