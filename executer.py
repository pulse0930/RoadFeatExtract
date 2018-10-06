import os
#all_content = os.listdir()
cwd = os.getcwd()
map_data_path = os.path.join(cwd,'Finalised_data')
roads_folder = os.path.join(cwd,'data')
code_file_path = os.path.join(cwd,'code_files')
all_content = os.listdir()
print(all_content)
count = 0
for content in all_content:
	if content.find('Date') >=0:
		os.chdir(content)
		inner_contents = os.listdir()
		for inner_content in inner_contents:
			print("\n# " + content + " " + inner_content + "\n")
			try:
				if inner_content.find('DATA') >=0:
					os.chdir(inner_content)
					os.chdir('All')
					files = os.listdir()
					GPS = None
					WiFi = None
					ACC = None
					SOUND = None
					PROACC = None
					PROSOUND = None
					for file in files:
						if file.find('GPS')>-1:
							GPS = file
						if file.find('WiFi')>-1:
							WiFi = file
						if file.find('_ACC')>-1:
							ACC = file
						if file.find('SOUND')>-1:
							SOUND = file
					count += 1
					command1 = 'python3 {} -o {} -sound {}'.format(os.path.join(code_file_path,'master_script.py'),os.getcwd(),os.path.abspath(SOUND))
					command2 = 'python3 {} -o {} -acc {}'.format(os.path.join(code_file_path,'master_script.py'),os.getcwd(),os.path.abspath(ACC))
					command3 = 'python3 {} -o {} -merge {} {} {} {} {}'.format(os.path.join(code_file_path,'master_script.py'),os.getcwd(),os.path.abspath(GPS),os.path.abspath(WiFi),os.path.abspath('processed_'+ACC),os.path.abspath('processed_'+SOUND[:-3]+'txt'),os.path.abspath('merged.json'))
					command4 = 'python3 {} -o {} -exf {} {} {} {} {}'.format(os.path.join(code_file_path,'master_script.py'),os.getcwd(),os.path.abspath('merged.json'),os.path.join(map_data_path,'grid_nitkb.p'),os.path.join(map_data_path,'NITKBLandmarks.json'),os.path.join(map_data_path,'intersection_db.json'),os.path.abspath('features.csv'))
					# print(command1)
					# print(command2)
					# print(command3)
					# print(command4)
					# print('Processing sound data..')
					# os.system(command1)
					# print('Processing accelerometer data..')
					# os.system(command2)
					# print('Merging all..')
					# os.system(command3)
					print('Extracting features')
					os.system(command4)
					os.chdir('../..')

			except Exception as e:
				print("#"+str(e))
				# raise e
		print('Total Trail files processed:',count)
		os.chdir(cwd)
