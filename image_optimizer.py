import os, sys, Image, getopt, json
from os import listdir
from os.path import isfile, join

def main(argv):
	inputdirectory = os.getcwd() + '/'
	outputdirectory = os.getcwd() + '/optimized/'
	basepath = os.path.dirname(__file__)
	config_path = 'config.json'
	if len(basepath) > 0:
		config_path = basepath + '/config.json'
	
	json_data=open(config_path) 
	config = json.load(json_data)
	json_data.close()
	quality = config['quality']
	extensions = config['extensions']
	change_extensions = config['change_extensions']['value']
	try:
		opts, args = getopt.getopt(argv,"hi:o:q:",["ifile=","ofile=","qfile="])
	except getopt.GetoptError:
		print 'image_optimizer.py -i <inputdirectorypath> -o <outputdirectorypath> -q <imagequality>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
	 		print 'image_optimizer.py -i <inputdirectorypath> -o <outputdirectorypath> -q <imagequality>'
	 		sys.exit()
		elif opt in ("-i", "--ifile"):
	 		inputdirectory = arg
			if inputdirectory[-1] != '/':
				inputdirectory += '/'

		elif opt in ("-o", "--ofile"):
			outputdirectory = arg
			if outputdirectory[-1] != '/':
				outputdirectory += '/'
		elif opt in ("-q", "--qfile"):
			quality = int(arg)

	if not os.path.exists(outputdirectory):
		os.makedirs(outputdirectory)
	print 'Input directory is >', inputdirectory
	print 'Output directory is >', outputdirectory
	print('starting!')
	print('............................................')
	all_images = [f for f in listdir(inputdirectory[0:-1]) if any(f.endswith(ext) for ext in extensions)]
	for image in all_images:
		if change_extensions:
			file_ext = change_extensions
		else:	
			file_ext = image.split('.')[-1]
		new_image = image.split('.')[0] +'.'+file_ext
		try:
			im = Image.open(inputdirectory + image)
			im.save(outputdirectory + new_image, 'JPEG' if file_ext  == 'jpg' else file_ext, quality=quality)
			print('optimizing image \n"%s" to \n"%s"') % (image, new_image)
		except IOError, e:
			print "cannot optimize file'%s', \nerror message %s" % (image, unicode(e))
	print('............................................')
	print('done!')
	print('############################################')
	print('optimized from %s') % inputdirectory
	print('optimized to %s') % outputdirectory
	print('images  %s') % len(all_images)
	print('############################################')

if __name__ == "__main__":
	main(sys.argv[1:])