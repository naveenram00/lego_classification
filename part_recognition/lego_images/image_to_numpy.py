import os

from PIL import Image
import numpy as np

#Directory containing images you wish to convert
input_dir = "/usr/src/lego_classification/part_recognition/lego_images/train"

directories = os.listdir(input_dir)
directories = sorted(directories)

index = 0
index2 = 0

for folder in directories:
	#Ignoring .DS_Store dir
	if folder.lower() == '.ds_store':
		pass

	else:
		print folder

		folder2 = os.listdir(input_dir + '/' + folder)
		index += 1

		for image in folder2:
			if image.lower() == ".ds_store":
				pass

			else:
				index2 += 1

				im = Image.open(input_dir+"/"+folder+"/"+image) #Opening image
				im = im.resize((32, 32), Image.ANTIALIAS)
				
				if im.mode == 'RGBA':
					print("Mode:" + im.mode)
					print image
					#im = im.convert('RBG')
					#im.save(image.toString() + ".jpg")
					
					im.load() # required for png.split()

					background = Image.new("RGB", im.size, (255, 255, 255))
					background.paste(im, mask=im.split()[3]) # 3 is the alpha channel

					background.save(image + '.jpg', 'JPEG', quality=80)
					im = background

				if im.mode == 'L':

					rgbim = Image.new("RGB", im.size)
					rgbim.paste(im)
					im = rgbim

				#print(im.size)
				im = (np.array(im)) #Converting to numpy array

				
				try:
					r = im[:,:,0] #Slicing to get R data
					g = im[:,:,1] #Slicing to get G data
					b = im[:,:,2] #Slicing to get B data

					if index2 != 1:
						new_array = np.array([[r] + [g] + [b]], np.uint8) #Creating array with shape (3, 100, 100)
						out = np.append(out, new_array, 0) #Adding new image to array shape of (x, 3, 100, 100) where x is image number

					elif index2 == 1:
						out = np.array([[r] + [g] + [b]], np.uint8) #Creating array with shape (3, 100, 100)

					if index == 1 and index2 == 1:
						index_array = np.array([[index-1]])

					else:
						new_index_array = np.array([[index-1]], np.int8)
						index_array = np.append(index_array, new_index_array, 0)

				except Exception as e:
					print e
					print "Removing image" + image
					#os.remove(input_dir+"/"+folder+"/"+image)

#print index

np.save(os.path.join('processed_data', 'X_train.npy'), out)
np.save(os.path.join('processed_data', 'Y_train.npy'), index_array) #Saving train labels

print index_array
print "--------------------"
print len(out)
print len(index_array)
#print out

#str1 = ''.join(str(e) for e in out)
#print str1
#print(index_array)
