from chpdb import cursor
from model.misfirecluster import MisfireCluster
import datetime
import pickle


cursor.execute('SELECT id FROM anlaeg')
machineIDresults = cursor.fetchall()
misfireClusters = []
count = 0
for machineIDresult in machineIDresults:
    count+=1
    print(str(count) + ' of ' + str(len(machineIDresults)))
    machineID = machineIDresult[0]
    cursor.execute('SELECT dato FROM anlaegshaendelser WHERE haendelse=112 AND anlaeg_id='+str(machineID) + ' ORDER BY dato')
    results = cursor.fetchall()
    if len(results) < 1:
        continue
    lastMisfire = datetime.datetime.min
    
    for result in results:
        date = result[0]
        if (date - lastMisfire) > datetime.timedelta(hours = 5):
            lastMisfire = date
            misfireClusters.append(MisfireCluster(machineID =machineID, date = lastMisfire, duration = datetime.timedelta(seconds = 0), count = 1))
            continue
        else:
            misfireClusters[-1].addMisfire(date)    

f = open('data/clusters.rick', 'wb')
pickle.dump(misfireClusters, f)
f.close()


