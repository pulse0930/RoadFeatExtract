from landmarks import *
import ast
from intersections import intersection
from progress import printProgressBar
''' R : RMS of z accelerations
    V : real-time speed of the vehicle at the location of the i-th acceleration measurement.'''
def iri_proxy(R, n, V):
    speed_sums = np.sum(V)
    iri_value = ((n * R ) / speed_sums ) * 100
    if  0 <= iri_value and iri_value < 2:
        return 1,iri_value     #excellent/good'''
    elif  2 <= iri_value and iri_value < 4:
        return 2,iri_value    #fair
    elif  4 <= iri_value and iri_value < 9:
        return 3,iri_value     #poor
    return 4,iri_value    #bad/failed

def extract_features(l,data,out_file,clustered_junction,intersection_db,way_folder):
    i=-1
    prev = None
    move = False
    file = open(out_file,'w')
    file.write('TimeStamp,Start Lat,Start Lng,End Lat,End Lng,Intersections,Segment Length,Mean speed,SD speed,Honks,WiFis,Segment len__,RSI,gps_counts\n')
    flow = []
    sounds = []
    wifi_dict = {}
    tss = list(data.keys())
    for ts in tss:
        i+=1
        #print(i)
        gps = data[ts]['gpss']
        res = l.check(gps[0],gps[1],25)
        if(prev is None and res[0]):
            prev = res
            move = False
        else:
            last = move
            move = not res[0]
            dist_covered = get_spherical_distance(gps[0],data[tss[i-1]]['gpss'][0],gps[1],data[tss[i-1]]['gpss'][1])
            if not move == last:
                if(move):
                    flow = []
                    sounds = []
                    wifi_dict = {}
                    z = []
                    n = []
                    speeds = []
                    gps_points = []
                else:
                    honks = (np.array(sounds)>80).sum()
                    time_taken = len(sounds)
                    sound_data = 0
                    try:
                        sound_data = float(honks)/time_taken
                    except Exception as e:
                        sound_data = 0
                    wifis_found = len(wifi_dict)
                    intersection_info = intersection(prev[1],prev[2],res[1],res[2],clustered_junction,way_folder,intersection_db)
                    startLat = prev[1]
                    startLng = prev[2]
                    endLat = res[1]
                    endLng = res[2]
                    intersection_count = intersection_info['count']
                    segment_len = np.sum(flow)
                    segment_len_ = get_spherical_distance(startLat,endLat,startLng,endLng)
                    mean_speed = np.mean(flow)
                    std_speed = np.std(flow)
                    RSI = iri_proxy(np.sqrt(np.sum(z)/np.sum(n)),np.sum(n),speeds)
                    file.write(ts+','+str(startLat)+','+str(startLng)+','+str(endLat)+','+str(endLng)+','+str(intersection_count)+','+str(segment_len)+','+str(mean_speed)+','+str(std_speed)+','+str(sound_data)+','+str(wifis_found)+','+str(segment_len_)+','+str(RSI[1])+','+str(len(gps_points))+'\n')
                    with open('RSI_{0}.txt'.format(str(RSI[0])), 'a+') as outf:
                        for g in gps_points:
                            outf.write('{0},{1}\n'.format(str(g[0]),str(g[1])))
                    prev = res

            else:
                if(move):
                    flow.append(dist_covered)
                    sounds.append(data[ts]['sounds'])
                    gps_points.append(data[ts]['gpss'])
                    z.append(data[ts]['accs'])
                    n.append(data[ts]['len_acc'])
                    speeds.append(data[ts]['speed_acc'])
                for wifi in data[ts]['wifis']:
                    wifi_dict[wifi] = True
        printProgressBar(i,len(tss)-1)
    file.close()

if __name__ == '__main__':
    # import json
    # f = open("./recodelinks/all_junctions.json",'r')
    # landmarks = json.loads(f.read())
    # f.close()
    # file = open('all_landmarks_filtered_dgp.txt','w')
    # print(landmarks)
    # bounds = [23.4523467,23.6789802,87.2019191,87.4475261]
    # landmark_array = []
    # for landmark in landmarks:
    # 	if (landmark['lat']>bounds[0] and landmark['lat']<bounds[1] and landmark['lng']>bounds[2] and landmark['lng']<bounds[3]):
    # 		file.write(str(landmark['lat'])+','+str(landmark['lng'])+'\n')
    # 		landmark_array.append([landmark['lat'],landmark['lng']])
    # print(np.array(landmark_array))
    # file.close()

    # import os
    # from DBSCAN import *

    l = Landmarks('dgp60', dim = 100, bounds = [23.4523467,23.6789802,87.2019191,87.4475261])
    l.form_tree()
    testing(l)
