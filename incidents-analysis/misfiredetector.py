from chpdb import cursor
from model.misfirecluster import MisfireCluster
import datetime
import pickle

f = open('data/clusters-5min.rick', 'wb')

cursor.execute('SELECT DISTINCT anlaeg_id FROM anlaegshaendelser;')
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
        if (date - lastMisfire) > datetime.timedelta(minutes=5):
            lastMisfire = date
            misfireClusters.append(MisfireCluster(machineID =machineID, date = lastMisfire, duration = datetime.timedelta(seconds = 0), count = 1))
            continue
        else:
            lastMisfire = date
            misfireClusters[-1].addMisfire(date)

pickle.dump(misfireClusters, f)
f.close()


