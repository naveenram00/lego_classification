
import os

input_dir = "/usr/src/lego_classification/part_recognition/lego_images/6k"
dest_dir =  "/usr/src/lego_classification/part_recognition/lego_images/train"

def listdir_nohidden(path):
	files = os.listdir(path)
	for f in files:
		if f.startswith('.'):
			files.remove(f)
	return files


directories = listdir_nohidden(input_dir)
for folder in directories:
	#Ignoring .DS_Store dir
	if folder.lower() == '.ds_store':
		pass

	else:
		print folder

		files = listdir_nohidden(input_dir + '/' + folder)
		files = files[0:1000]

		for image in files:
			if folder.lower() == '.ds_store':
				pass

			else:
				source = input_dir + "/" + folder + "/" + image
				destination = dest_dir + "/" + folder + "/" + image

				print "folder: " + folder + " image: " + image
				#print source
				#print destination
				os.rename(source, destination)