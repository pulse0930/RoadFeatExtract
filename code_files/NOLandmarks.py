import json
from landmarks import *
def extract_features(data):
    d = 0
    i = 1
    tss = list(data.keys())
    gps_point=[]
    for ts in tss[1:]:
        if d >= 200:
            gps_point.append((data[tss[i]]['gpss'][0],data[tss[i]]['gpss'][1]))
            d = 0
        else:
            d += get_spherical_distance(data[tss[i]]['gpss'][0],data[tss[i-1]]['gpss'][0],data[tss[i]]['gpss'][1],data[tss[i-1]]['gpss'][1])
        i += 1
    for i in gps_point:
        print(i)

def main():
    trail_file = '/mnt/c/Users/Pallav/Desktop/projkt/merged.json'
    file = open(trail_file)
    data = json.loads(file.read())
    extract_features(data)
if __name__ == '__main__':
    main()
