
import os

from PIL import Image
import numpy as np
#input_dir = "/usr/src/lego_classification/part_recognition/lego_images/image_type_testing"
input_dir = "/usr/src/lego_classification/part_recognition/lego_images/lego_images_copy"


def listdir_nohidden(path):
	#Returns a list without hidden files
	files = os.listdir(path)
	for f in files:
		if f.startswith('.'):
			files.remove(f)
	return files


directories = listdir_nohidden(input_dir)
files_moved = 0
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
				im = im.resize((32, 32), Image.ANTIALIAS)
				print "IMAGE: " + image
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

