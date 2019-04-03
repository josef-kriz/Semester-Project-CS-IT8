from chpdb import cursor
from model.misfirecluster import MisfireCluster
import datetime
import pickle
cursor.execute('SELECT id FROM anlaeg')
machineIDresults = cursor.fetchall()
count = 0
for machineIDresult in machineIDresults:
    count+=1
    print(str(count) + ' of ' + str(len(machineIDresults)))
    machineID = machineIDresult[0]
    cursor.execute('SELECT dato FROM anlaegshaendelser WHERE haendelse=112 AND anlaeg_id='+str(machineID) + ' ORDER BY dato')
    print(cursor.statement)
    results = cursor.fetchall()
    if len(results) < 2:
        continue
    misfireClusters = []
    iterator = results.__iter__()
    lastMisfire = iterator.__next__()[0]
    currentlyCluster = False
    for result in iterator:
        date = result[0]
        if (date - lastMisfire) > datetime.timedelta(hours = 5):
            currentlyCluster = False
            lastMisfire = date
            continue
        if currentlyCluster:
            misfireClusters[-1].addMisfire(date)
        else:
            misfireClusters.append(MisfireCluster(machineID =machineID, date = lastMisfire, duration = date - lastMisfire, count = 2))
        currentlyCluster = True
    
    f = open('misfireClusters/' + str(machineID) + '_clusters.rick', 'wb')
    pickle.dump(misfireClusters, f)
    f.close()
 


