
import os

from PIL import Image, ImageChops
import numpy as np
#input_dir = "/usr/src/lego_classification/part_recognition/lego_images/crop_testing"
#input_dir = "/usr/src/lego_classification/part_recognition/lego_images/lego_images_copy"
input_dir = "/usr/src/lego_images_cropped"

def png_to_array(path):
	im = Image.open(path)
	if im.mode == 'RGBA':
		print("Mode:" + im.mode)
		
		#im = im.convert('RBG')
		#im.save(image.toString() + ".jpg")
		
		im.load() # required for png.split()

		background = Image.new("RGB", im.size, (255, 255, 255))
		background.paste(im, mask=im.split()[3]) # 3 is the alpha channel

		#background.save(image + '.jpg', 'JPEG', quality=80)
		im = background

	if im.mode == 'L':

		rgbim = Image.new("RGB", im.size)
		rgbim.paste(im)
		im = rgbim
	im = crop_white(im)
	im = make_square(im)
	im = im.resize((32, 32), Image.ANTIALIAS)
	im = (np.array(im))

	r = im[:,:,0] #Slicing to get R data
	g = im[:,:,1] #Slicing to get G data
	b = im[:,:,2] #Slicing to get B data

	out = np.array([r] + [g] + [b],np.uint8)
	return out

def resize_square(path, size):
	im = Image.open(file)	
	im = crop_white(im)
	im = make_square(im)
	im = im.resize((32, 32), Image.ANTIALIAS)
	im.save(path)


def listdir_nohidden(path):
	#Returns a list without hidden files
	files = os.listdir(path)
	for f in files:
		if f.startswith('.'):
			files.remove(f)
	return files

def test(file):
	im = Image.open(file)
	#im = crop_white(im)
	im = make_square(im)
	im.save(file)

def crop_white (im):
	bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
	diff = ImageChops.difference(im, bg)
	diff = ImageChops.add(diff, diff, 2.0, -100)
	bbox = diff.getbbox()
	if bbox:
		return im.crop(bbox)
	else:
		print im.format
		return im

def make_square(im):

	fill_color = (255, 255, 255, 0)

	x, y = im.size
	size = max(x, y)
	new_im = Image.new('RGBA', (size, size), fill_color)
	new_im.paste(im, ((size - x) / 2, (size - y) / 2))
	return new_im

def resize_all():
	directories = listdir_nohidden(input_dir)
	print input_dir
	print directories
	for folder in directories:
	#Ignoring .DS_Store dir
		if folder.lower() == '.ds_store':
			pass

		else:
			print folder

			files = listdir_nohidden(input_dir + '/' + folder)

			for image in files:
				if folder.lower() == '.ds_store':
					pass

				else:

					path = input_dir + "/" + folder + "/" + image
					im = Image.open(input_dir+"/"+folder+"/"+image) #Opening image
					im = make_square(im)
					im = im.resize((32, 32), Image.ANTIALIAS)
					#print "IMAGE: " + image
					if im.mode == 'RGBA':
						print("Mode:" + im.mode)
						#print image
						#im = im.convert('RBG')
						#im.save(image.toString() + ".jpg")
						
						im.load() # required for png.split()

						background = Image.new("RGB", im.size, (255, 255, 255))
						background.paste(im, mask=im.split()[3]) # 3 is the alpha channel

						#background.save(image + '.jpg', 'JPEG', quality=80)
						im = background

					if im.mode == 'L':

						rgbim = Image.new("RGB", im.size)
						rgbim.paste(im)
						im = rgbim
					
					os.remove(path)
					im.save(path[:-4] + ".jpg")

					# print path
					# print path[:-4] + ".jpg"
					# print "---"

def crop_all():
	directories = listdir_nohidden(input_dir)
	for folder in directories:
		#Ignoring .DS_Store dir
		if folder.lower() == '.ds_store':
			pass

		else:
			index = 0
			print folder

			files = listdir_nohidden(input_dir + '/' + folder)

			for image in files:
				if folder.lower() == '.ds_store':
					pass

				else:

					if index % 100 == 0:
						print index
					index += 1

					path = input_dir + "/" + folder + "/" + image

					if path[-4:] != ".jpg":
						im = Image.open(path) #Opening image

						im = crop_white(im)

						im.save(path)

