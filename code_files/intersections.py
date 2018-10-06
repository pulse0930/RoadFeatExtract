import json
import os

def intersection(start_lat, start_lng, end_lat, end_lng, clustered_junctions, way_folder, store_file = None):

	# if start_lat > end_lat:
	# 	x1 = start_lat
	# 	x2 = end_lat
	# else:
	# 	x1 = end_lat
	# 	x2 = start_lat

	# if start_lng > end_lng:
	# 	y1 = 

	# fileLoc2 = os.getcwd()+"/bike_data.json"
	# fileLoc_highways = os.getcwd()+"/data2/"
	# req_filLoc1 = ""
	# req_filLoc2 = ""
	stored_data = {}
	format_string = "{}_{}_{}_{}".format(start_lat,start_lng,end_lat,end_lng)
	if not store_file is None:
		try:
			file = open(store_file,'r')
			stored_data = json.loads(file.read())
			file.close()
			if(format_string in stored_data.keys()):
				return stored_data[format_string]
		except Exception as e:
			pass
		

	Arr=[]
	perr=[]
	i = 0
	j=0
	k=0
	l=0
	
	dgp_array = clustered_junctions
	
	

	f= open(os.path.join(way_folder,"living_street.json"), 'r')
	q= json.loads(f.read())
	f.close()


	details1=[]
	details2=[]	
	emptyArr=[]
	req_array=[]
	obj={}
	obj['nodesKey']=[]
	obj['count'] = 0
	i=0
	j=0
	wayId=0
	fileNm=""
	for dgp_obj1 in dgp_array:
		if float(start_lat) == dgp_obj1["center_lat"] and float(start_lng) == dgp_obj1["center_lng"]:
			details1=dgp_obj1["details"]
			break
	for dgp_obj2 in dgp_array:
		if float(end_lat) == dgp_obj2["center_lat"] and float(end_lng) == dgp_obj2["center_lng"]:
			details2=dgp_obj2["details"]
			break
	while(i<len(details1)):
		j=0
		while(j<len(details2)):

			if (details1[i][2]==details2[j][2] or details1[i][2]==details2[j][3]) and (details1[i][2]!=-1 or details2[j][2]!=-1) :
				wayId=details1[i][2]
				fileNm=details1[i][4]
				det_start_lat=details1[i][0]
				det_start_lng=details1[i][1]
				det_end_lat=details2[j][0]
				det_end_lng=details2[j][1]

			elif (details1[i][3]==details2[j][2] or details1[i][3]==details2[j][3]) and (details1[i][2]!=-1 or details2[j][2]!=-1):
				wayId=details1[i][3]
				fileNm=details1[i][4]				
				det_start_lat=details1[i][0]
				det_start_lng=details1[i][1]
				det_end_lat=details2[j][0]
				det_end_lng=details2[j][1]


			if wayId != 0:				
				obj['id']=wayId
				obj['fn']=fileNm			
				f=open(os.path.join(way_folder,fileNm))
				p = json.loads(f.read())
				f.close
				for way in p:
					if float(way['id'])==wayId:
						for index,node in enumerate(way['nodesKey']):
							if (node['lat'] == det_start_lat and node['lng']==det_start_lng):
								k=index
							if (node['lat']==det_end_lat and node['lng']==det_end_lng):
								l=index
						if k>l:
							req_array = way['nodesKey'][l:k+1]
						else:
							req_array = way['nodesKey'][k:l+1]


						break

			j=j+1
		i=i+1

	for node in req_array:
			for living_way in q:
				for l_node in living_way['nodesKey']:
					if node == l_node:
						obj['nodesKey'].append(node)
						obj['count']=len(obj['nodesKey'])

	
	# Arr.append(obj)

	if not store_file is None:
		file = open(store_file,'w')
		stored_data[format_string] = obj
		file.write(json.dumps(stored_data))
		file.close()

	return obj

if __name__ == '__main__':
	# fileLoc1 = os.getcwd()+"/dgp60.json"

	f_dgp = open('../Finalised_data/clustered_junction.json','r')
	clustered_junctions_array = json.loads(f_dgp.read())
	f_dgp.close()
	print(intersection(23.5463329,87.2928642,23.5499942,87.2953886,clustered_junctions_array,'../data'))














