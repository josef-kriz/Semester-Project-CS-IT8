from model.misfirecluster import MisfireCluster
from datetime import timedelta
import pickle
import sys

data =[]
intervalDuration = timedelta()

try:
    intervalDuration = timedelta(seconds = int(sys.argv[2]))
    data = pickle.load(open(sys.argv[1], "rb"))
except:
    print("First argument must be path to the file with misfire cluster data, "
          "second argument must be grouping interval in seconds (or divider for modulo of count)."
          "Third argument is part to output file. Fourth argument is 'count' in case you want to"
          "group clusters into groups according the number of misfires in cluster.")

output = {}
# go through clusters and group them according to time or count interval
# single misfire events are excluded from grouping and inserted under the key 0
for cluster in data:
    if len(sys.argv) >= 5 and sys.argv[4] == 'count':
        if cluster.count == 1:
            index = 0
        else:
            index = int(cluster.count / int(sys.argv[2])) + 1
    else:
        if cluster.count == 1:
            index = 0
        else:
            index = int(cluster.duration / intervalDuration) + 1

    if index not in output:
        output[index] = [cluster]
    else:
        output[index].append(cluster)

# print statistics about the groups
if 0 in output and len(sys.argv) < 5:
    print('Singles:', len(output[0]))

groups = sorted(output.items(), key=(lambda x: x[0]))
for index, group in groups:
    if index == 0 and len(sys.argv) < 5:
        continue
    if len(sys.argv) >= 5 and sys.argv[4] == 'count':
        print("Clusters of length", index * int(sys.argv[2]), "to", (index + 1) * int(sys.argv[2]), ":", len(group))
    else:
        print(str((index-1)*intervalDuration), 'to', str(index * intervalDuration), ':', len(group))

# store groups in a pickle format file
f = open(sys.argv[3], 'wb')
pickle.dump(output, f)
f.close()
