import numpy as np
from math import *
# from DBSCAN import get_spherical_distance
#import matplotlib.pyplot as plt
def get_spherical_distance(lat1,lat2,long1,long2):
        """
        Get spherical distance any two points given their co-ordinates (latitude, longitude)
        """
        q=radians(lat2-lat1)
        r=radians(long2-long1)
        lat2r=radians(lat2)
        lat1r=radians(lat1)
        a=sin(q/2)*sin(q/2)+cos(lat1r)*cos(lat2r)*sin(r/2)*sin(r/2)
        c=2*atan2(sqrt(a),sqrt(1-a))
        R=6371*1000
        d=R*c
        return d
class Node(object):
	"""docstring for Node"""
	def __init__(self,lat,lng, rad = 0,ne= None,nw= None,sw= None,se= None):
		self.isLeaf = True
		self.lat = lat
		self.long = lng
		self.NE = ne
		self.NW = nw
		self.SW = sw
		self.SE = se
		self.radi = rad
		# if not par == None:
		# 	if(par.lat>lat):
		# 		if(par.long>lng):
		# 			par.ne = self
		# 		else:
		# 			par.nw = self
		# 	else:
		# 		if(par.long>lng):
		# 			par.se = self
		# 		else:
		# 			par.sw = self
	def get_distance(self,lat,lng):
		return get_spherical_distance(self.lat,lat,self.long,lng)

class Landmarks(object):
	"""docstring for Landmarks"""
	def __init__(self, data = None, file_path = None, dim = 10, bounds = None):
		# super(Landmarks, self).__init__()
		if not file_path is None:
			self.landmarks = np.loadtxt(file_path,delimiter=',',usecols=(0,1,2))
		if not data is None:
			self.landmarks = np.array(data)
		self.tree = None
		self.grid = None
		self.dim = dim
		if not bounds is None:
			filtered_landmarks = []
			for landmark in self.landmarks:
				if (landmark[0]>bounds[0] and landmark[0]<bounds[1] and landmark[1]>bounds[2] and landmark[1]<bounds[3]):
					filtered_landmarks.append(landmark)
			self.landmarks = np.array(filtered_landmarks)
		self.maxes = np.max(self.landmarks,0)
		self.mins = np.min(self.landmarks,0)
		self.boundary_size = self.maxes-self.mins
		self.cell_size = self.boundary_size/dim
		locations_lat = np.floor((self.landmarks[:,0] - self.mins[0])/self.cell_size[0])
		locations_lng = np.floor((self.landmarks[:,1] - self.mins[1])/self.cell_size[1])
		location_in_grid = np.vstack([locations_lat,locations_lng])
		location_in_grid[location_in_grid == dim] = dim-1
#		plt.scatter(locations_lat,locations_lng)
#		plt.show()
		#print(location_in_grid)
		self.grid = [None]*dim
		self.grid_tree = [None]*dim
		# print(self.grid)
		i=0
		for loc in location_in_grid.T:
			if self.grid[int(loc[0])] == None:
				self.grid[int(loc[0])] = [None]*dim
			if self.grid[int(loc[0])][int(loc[1])] == None:
				self.grid[int(loc[0])][int(loc[1])] =[]
			self.grid[int(loc[0])][int(loc[1])].append(self.landmarks[i])
			i+=1
       #print(self.grid)
		# import pickle
		# pickle.dump(self.grid,open('grid.p','wb'))
		# print(np.min(self.landmarks[:,0]),np.min(self.landmarks[:,1]),np.max(self.landmarks[:,0]),np.max(self.landmarks[:,1]))

	def form_tree(self):
		max_size = 0
		i = -1
		for rows in self.grid:
			i+=1
			j=-1
			if rows == None:
				continue
			for items in rows:
				if(self.grid_tree[i]==None):
					self.grid_tree[i] = [None]*self.dim
				j+=1
				if items == None:
					continue
					j+=1
				else:
					#print(items)
					if len(items)>max_size:
						max_size = len(items)

					land_center = np.mean(items,0)
					print(land_center)
					# self.tree = Node(land_center[0],land_center[1])
					self.grid_tree[i][j] = self.construct_node(items)
					# print(self.tree)
					# break
			# break
		print('Max size: ',max_size)
		# print(self.grid_tree)

	def construct_node(self, data_set):
		data_set = np.array(data_set)
		if(len(data_set)<1):
			return None
		if(len(data_set) == 1):
			return Node(data_set[0][0],data_set[0][1],data_set[0][2])
		land_center = np.mean(data_set,0)
		# print(land_center,'*************************')
		ne = data_set[(data_set[:,0]>=land_center[0]) & (data_set[:,1]>=land_center[1])]
		nw = data_set[(data_set[:,0]>=land_center[0]) & (data_set[:,1]<land_center[1])]
		se = data_set[(data_set[:,0]<land_center[0]) & (data_set[:,1]>=land_center[1])]
		sw = data_set[(data_set[:,0]<land_center[0]) & (data_set[:,1]<land_center[1])]
		node = Node(land_center[0],land_center[1])
		node.isLeaf = False
		node.NE = self.construct_node(ne)
		node.NW = self.construct_node(nw)
		node.SE = self.construct_node(se)
		node.SW = self.construct_node(sw)
		return node

	def check(self,lat,lng,radius):
		#print(self.mins,self.cell_size)
		cell_lat = int((lat-self.mins[0])/self.cell_size[0])
		cell_lng = int((lng-self.mins[1])/self.cell_size[1])
		if cell_lat == self.dim:
			cell_lat = self.dim-1
		if cell_lng == self.dim:
			cell_lng = self.dim-1
		#print(lat,lng,cell_lat,cell_lng,self.dim)
		#print(self.grid[cell_lat][cell_lng])
		if cell_lat >= 0 and cell_lat < self.dim and cell_lng >= 0 and cell_lng < self.dim and not(self.grid[cell_lat] == None or self.grid[cell_lat][cell_lng] == None):
			for landmark in self.grid[cell_lat][cell_lng]:
				if (radius + landmark[2]) > get_spherical_distance(lat,landmark[0],lng,landmark[1]):
					#print(get_spherical_distance(lat,landmark[0],lng,landmark[1]))
					return (True, landmark[0], landmark[1])
		if cell_lat-1 >= 0 and cell_lat < self.dim and cell_lng >= 0 and cell_lng < self.dim and not(self.grid[cell_lat-1] == None or self.grid[cell_lat-1][cell_lng] == None):
			for landmark in self.grid[cell_lat-1][cell_lng]:
				if (radius + landmark[2]) > get_spherical_distance(lat,landmark[0],lng,landmark[1]):
					#print(get_spherical_distance(lat,landmark[0],lng,landmark[1]))
					return (True, landmark[0], landmark[1])
		if cell_lat >= 0 and cell_lat < self.dim and cell_lng-1 >= 0 and cell_lng < self.dim and not(self.grid[cell_lat] == None or self.grid[cell_lat][cell_lng-1] == None):
			for landmark in self.grid[cell_lat][cell_lng-1]:
				if (radius + landmark[2]) > get_spherical_distance(lat,landmark[0],lng,landmark[1]):
					#print(get_spherical_distance(lat,landmark[0],lng,landmark[1]))
					return (True, landmark[0], landmark[1])
		if cell_lat >= 0 and cell_lat+1 < self.dim and cell_lng >= 0 and cell_lng < self.dim and not(self.grid[cell_lat+1] == None or self.grid[cell_lat+1][cell_lng] == None):
			for landmark in self.grid[cell_lat+1][cell_lng]:
				if (radius + landmark[2]) > get_spherical_distance(lat,landmark[0],lng,landmark[1]):
					#print(get_spherical_distance(lat,landmark[0],lng,landmark[1]))
					return (True, landmark[0], landmark[1])
		if cell_lat >=0 and cell_lat < self.dim and cell_lng >= 0 and cell_lng+1 < self.dim and not(self.grid[cell_lat] == None or self.grid[cell_lat][cell_lng+1] == None):
			for landmark in self.grid[cell_lat][cell_lng+1]:
				if (radius + landmark[2]) > get_spherical_distance(lat,landmark[0],lng,landmark[1]):
					#print(get_spherical_distance(lat,landmark[0],lng,landmark[1]))
					return (True, landmark[0], landmark[1])
		return (False,)

		# if(self.grid_tree[cell_lat][cell_lng] == None):
		# 	return (False)
		# else:
		# 	temp = self.grid_tree[cell_lat][cell_lng]
		# 	while(not temp.isLeaf):
		# 		print(temp.lat,temp.long)
		# 		if (lat>=temp.lat):
		# 			if(lng>=temp.long):
		# 				temp= temp.NE
		# 			else:
		# 				temp = temp.NW
		# 		else:
		# 			if(lng>=temp.long):
		# 				temp= temp.SE
		# 			else:
		# 				temp = temp.SW
		# 		if(temp == None):
		# 			return(False)
		# 	return (True,temp.lat,temp.long)
def save_as(l,name):
	import pickle
	pickle_out = open(name,"wb")
	pickle.dump(l, pickle_out)
	pickle_out.close()

if __name__ == '__main__':
    import json
    inp_file = open('../Finalised_data/NITKBLandmarks.json')
    junction_info = json.loads(inp_file.read())
    inp_file.close()
    required = []
    for data in junction_info:
        required.append((data['center_lat'],data['center_lng'],data['center_span']))
    l = Landmarks(data = np.array(required),dim = 100)
	# 23.640226124694472,87.2265715234268
#	l = Landmarks('dgp60',dim = 100, bounds = [23.4523467,23.6789802,87.2019191,87.4475261])
 #   l.form_tree()
    print(l.dim)
    print(l.check(23.56407967,87.28199015,25))
#	# 23.6402309,87.226513
