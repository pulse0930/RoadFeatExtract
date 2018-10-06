# acc_data_merge.py
import numpy as np
import sys
import os
from progress import printProgressBar
from acccorrect import accelerometer_correction
try:
	filename = sys.argv[1]
	folder = sys.argv[2]
except Exception as e:
	filename = 'Scooty_ACC_2018_05_25_15_16_52_15.txt'

datatype=np.dtype([('time','S20')])
data_t = np.loadtxt(filename,usecols=(3),dtype = datatype, delimiter=',',skiprows=1)
data = np.loadtxt(filename,usecols=(0,1,2),delimiter=',',skiprows=1)

pwd = os.getcwd()
os.chdir(folder)

frames = {}
i = 0
last = 0
start = 0
checker = None
#print(data_t)
#print(data.shape)
#counter = 0
size = len(data_t)

# A frame is time stamp : (startIndex,EndIndex)
for d in data_t:
	if d[0].decode() == checker:
		pass
	else:
		if checker is None:
			checker = d[0].decode()
		else:
			frames[checker] = (last,i)
			last = i-1
			checker = d[0].decode()
			# input()
	i+=1
	printProgressBar(i,size+len(frames.keys()))

file = open('processed_'+os.path.basename(filename),'w')
for frame in frames.keys():
	start,stop = frames[frame]
	now = np.array(data[start:stop])
	if len(now) < 10:
		now_ = now
	else:
		now_ = now[0:now.size:3] #down sampling
	sum_sqr_z = 0
	arr = []
	for acc_row in now_:
		r_x,r_y,r_z,x,y,z = accelerometer_correction(acc_row[0],acc_row[1],acc_row[2])
		sum_sqr_z += z*z
		arr.append(z)
	file.write(frame+','+str(z*z)+','+str(len(now_))+','+str(arr)+'\n')
	i+=1
	printProgressBar(i,size+len(frames.keys()))
file.close()
os.chdir(pwd)
