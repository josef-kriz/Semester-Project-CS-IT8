from model.misfirecluster import MisfireCluster
from datetime import timedelta
import pickle
import sys

data =[]
intervalDuration = timedelta()
try:
    intervalDuration = timedelta(seconds = int(sys.argv[2]))
    data = pickle.load(open(sys.argv[1], "rb"))
except: print("First argument must be path to the file with misfire cluster data, second argument must be grouping time interval in seconds")

output = [[]]
for cluster in data:
    if cluster.count == 1:
        output[0].append(cluster)
        continue
    interval = int(cluster.duration / intervalDuration) + 1
    while interval >= len(output):
        output.append([])
    output[interval].append(cluster) 
print('Singles:', len(output[0]) )
i = 1
while i<len(output):
    print(str((i-1)*intervalDuration), 'to', str(i* intervalDuration), ':', len(output[i]))
    i+=1
f = open('clustersgrouped.rick', 'wb')
pickle.dump(output, f)
f.close()


