import sys
import os
import numpy as np
import math
# print 'Starting NEMO------------------------------------------------------'

def get_spherical_distance(lat1,lat2,long1,long2):
        """
        Get spherical distance any two points given their co-ordinates (latitude, longitude)
        """
        q=math.radians(lat2-lat1)
        r=math.radians(long2-long1)
        lat2r=math.radians(lat2)
        lat1r=math.radians(lat1)
        a=math.sin(q/2)*math.sin(q/2)+math.cos(lat1r)*math.cos(lat2r)*math.sin(r/2)*math.sin(r/2)
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        R=6371*1000
        d=R*c
        return d

folder = ''
# try:
# 	folder = sys.argv[5]
# except Exception as e:
# 	print(e)

gps_file_name  = folder + sys.argv[1]
acc_file_name = folder + sys.argv[2]
out_file_name = folder + sys.argv[3]
out_folder = folder + sys.argv[4]

data = {}

datatype=np.dtype([('time','S20')])

gps_t = np.loadtxt(gps_file_name,usecols=(4),dtype = datatype, delimiter=',',skiprows=1)
gps = np.loadtxt(gps_file_name,usecols=(0,1),delimiter=',',skiprows=1)

acc_t = np.loadtxt(acc_file_name,usecols=(0),dtype = datatype, delimiter=',',skiprows=1)
acc = np.loadtxt(acc_file_name,usecols=(1,2),delimiter=',',skiprows=1)

# print(gps_t)
# input()
# print(acc_t)
# input()
# print(sound_t)

for i in range(len(gps_t)):
    try:
        data[gps_t[i][0].decode()] = {}
        data[gps_t[i][0].decode()]['accs'] = []
        data[gps_t[i][0].decode()]['gpss'] = list(gps[i])
        data[gps_t[i][0].decode()]['len'] = 0
        if i!=0:
        	data[gps_t[i][0].decode()]['speed'] = get_spherical_distance(gps[i][0],gps[i-1][0],gps[i][1],gps[i-1][1])
        else:
        	data[gps_t[i][0].decode()]['speed'] = 0
    except Exception as e:
        print(e)
		# raise(e)
# print(data.keys())

for i in range(len(acc_t)):
    try:
        if(acc_t[i][0].decode() not in data.keys()):
            continue
        data[acc_t[i][0].decode()]['accs'] = list(acc[i])[0]
        data[acc_t[i][0].decode()]['len'] = list(acc[i])[1]
        data[acc_t[i][0].decode()]['speed'] = data[acc_t[i][0].decode()]['speed'] * data[acc_t[i][0].decode()]['len']
    except Exception as e:
        print(e)

import json

outfile = os.path.join(out_folder,out_file_name)
file = open(outfile,'w')
file.write(json.dumps(data))
file.close()
