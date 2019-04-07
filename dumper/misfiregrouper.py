from model.misfirecluster import MisfireCluster
from datetime import timedelta
import pickle
import sys

data =[]
print(sys.argv)

try:
    data = pickle.load(open(sys.argv[1], "rb"))
    print(sys.argv[2], ' seconds')
except: print("First argument must be path to the file with misfire cluster data, second argument must be grouping time interval in seconds")

output = [[]]
for cluster in data:
    if cluster.count == 1:
        output[0].append(cluster)
        continue
    interval = int(cluster.duration / timedelta(seconds = int(sys.argv[2]))) + 1
    while interval >= len(output):
        output.append([])
    output[interval].append(cluster) 
print(output)
f = open('clustersgrouped.rick', 'wb')
pickle.dump(output, f)
f.close()


