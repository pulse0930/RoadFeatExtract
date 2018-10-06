#!/home/d/anaconda3/bin/python3
#/usr/bin/python3
# masterscript.py
import os
import sys
from progress import printProgressBar
import json
import numpy as np

if len(sys.argv) == 1:
	print('\tPlease provide proper input. Use -help for help.')
	exit(0)

pathname = os.path.dirname(sys.argv[0])

# The help part
if '-help' in sys.argv:
	print('\n\tFollow the following instructions for each step:')
	print('\n\t--To merge sound data from a wav file, use "-sound" switch followed by the filename of the wav file')
	print('\n\t--To merge accelerometer data from a file, use "-acc" switch followed\n\t  by the filename of the accelerometer data file')
	print('\n\t--To merge the gps, accelerometer and sound data files, use the "-merge" switch followed by the')
	print('\t  raw gps file, raw wifi file, processed accelerometer file and processed sound file and output file name.')
	print('\n\t--To extract features from the merged trail file, use "-exf" switch followed by the following')
	print('\t\t<merged trail file> <grid file> <clustered junction file> <a file name to store the information about smaller intersections> <output file name>')
	print('\n\t--To build the landmark model, use "-l" switch followed by the landmark json file and output file name.\n\t  the output json file will be stored in the out folder.')
	exit(0)

# Get the output folder name first.
out_folder = 'Finalised_data'
if '-o' in sys.argv:
	out_folder = sys.argv[sys.argv.index('-o') + 1]
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
else:
	print('\tOutputs will be stored in a folder named {0}.'.format(out_folder))

# Next step is to process the sound data and extract information into a flat file
# First each second in the wav file is filtered with frequencies ranging from
# 2000 to 5000 Hz. After that the frequency with highest intensity is recorded
# with its intensity value in a flat file with the same name having a "_processed"
# sufix.
if '-sound' in sys.argv:
	try:
		input_file = sys.argv[sys.argv.index('-sound') + 1]
		os.system('python3 ' + os.path.join(pathname, 'ips.py ') + input_file + ' ' + out_folder)

	except Exception as e:
		print('Please provide a wav file path after -sound')
		exit(1)

# Next we take the data form the accelerometer to express the data per second.
# The output file contains data in following format:
# timestamp,r_mean,r_std,x_mean,x_std,y_mean,y_std,z_mean,z_std,
# Where x,y and z represent the accelerations reccorded along the 3 axes of the phone
# and timestamp reecords the time in which the data is processed. r indicates the
# total applied acceleration calculated as sqrt(x^2 + y^2 +z^2)
if '-acc' in sys.argv:
	try:
		input_file = sys.argv[sys.argv.index('-acc') + 1]
		os.system('python3 ' + os.path.join(pathname, 'acc_data_merge.py ') + input_file + ' ' + out_folder)

	except Exception as e:
		print('Please provide a file path after -acc')
		exit(1)

# Merge data from different files into a single one
# Inputs are in sequence GPS, WiFi, processed ACC, processed Sound, output_file
if '-merge' in sys.argv:
	try:
		gps_file = sys.argv[sys.argv.index('-merge') + 1]
		wifi_file = sys.argv[sys.argv.index('-merge') + 2]
		acc_file = sys.argv[sys.argv.index('-merge') + 3]
		sound_file = sys.argv[sys.argv.index('-merge') + 4]
		out_file = sys.argv[sys.argv.index('-merge') + 5]

		os.system('python3 ' + os.path.join(pathname, 'merge.py ') + gps_file + ' ' \
			+ wifi_file + ' ' + acc_file + ' ' + sound_file \
			+ ' ' + out_file + ' ' + out_folder)
	except Exception as e:
		print('Please provide proper data after -merge. Look into help(-help) for details.')
		exit(1)

# This section is for feature extraction. For each segments that are identified we extract features
# such as Time taken,starting lat, starting lng, ending lat, ending lng, segment length, mean speed,
# standard deviation of speed, average accelerometer deviation, wifi density and observed honks. A segment
# is defined as the path between 2 road junctions. The method 'extract_features' takes parametes :
# grid_file data, trail_file data, output folder path, clustered_junctions data, intersection_db and
# way folder path and writes the extracted features in a csv file in the output folder path.

if '-exf' in sys.argv:
	try:
		import pickle
		from config import way_folder
		trail_file = sys.argv[sys.argv.index('-exf') + 1]
		grid_file = sys.argv[sys.argv.index('-exf') + 2]
		clustered_junction_file = sys.argv[sys.argv.index('-exf') + 3]
		intersection_db = sys.argv[sys.argv.index('-exf') + 4]
		out_file = sys.argv[sys.argv.index('-exf') + 5]

		file  = open(clustered_junction_file,'r')
		clustered_junctions = json.loads(file.read())
		file.close()

		from feature_extractor import extract_features
		pickle_in = open(grid_file,"rb")
		l = pickle.load(pickle_in)
		pickle_in.close()
		file = open(trail_file)
		data = json.loads(file.read())
		file.close()
		extract_features(l,data,os.path.join(out_folder,out_file),clustered_junctions,intersection_db,way_folder)
	except Exception as e:
		raise e

# Creating a grid of the clustered junctions. This is used to efficiently check if at a given point
# in trail, we are in the proximity of a junction or not. This section creates a model and saves it
# in a file named as the second command line parameter. The model, when loaded, provides a method
# that takes the current lat and long as input along with the distance in meters we define the notion
# of proximity. The method returns false if the point given is not near any of the the junctions and
# a tuple (True, lat, lng) where lat and lng are the latitude and longitude of the juction point the
# current point is nearest from.
if '-l' in sys.argv:
	try:
		inp_file = open(sys.argv[sys.argv.index('-l') + 1])
		out_file_name = sys.argv[sys.argv.index('-l') + 2]
		junction_info = json.loads(inp_file.read())
		inp_file.close()
		required = []
		for data in junction_info:
			required.append((data['center_lat'],data['center_lng'],data['center_span']))
		from landmarks import *
		l = Landmarks(data = np.array(required),dim=100)
		#l.form_tree()
		print(os.getcwd())
		save_as(l,os.path.join(out_folder,out_file_name))
	except Exception as e:
		print(e)
		print('Please provide proper json file after -l. Look into help(-help) for details.')
		exit(1)


if '-test' in sys.argv:
	import pickle
	grid_file = sys.argv[sys.argv.index('-test') + 1]
	pickle_in = open(grid_file,"rb")
	l = pickle.load(pickle_in)
	print(l)
