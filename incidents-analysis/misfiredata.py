from chpdb import cursor
import pickle
import datetime
from model.misfirecluster import MisfireCluster
from src.parser import parse_value
sensornames = ['actual_rpm']
incidents = [103, 101, 100, 102]

# queries the database for preceding incidents
def get_cluster_incidents(cursor, cluster, interval, haendelser = []):
    start = cluster.date - datetime.timedelta(seconds=interval)
    query = "SELECT haendelse, COUNT(*) FROM anlaegshaendelser " \
            " WHERE anlaeg_id = " + str(cluster.machineID) + " AND dato < \"" + str(cluster.date) + "\" AND " \
            " dato > \"" + str(start) + "\""
    if haendelser != []:
            query += " AND haendelse IN (" + str(haendelser[0])
            for i in range(1, len(haendelser)):
                query += ", " + str(haendelser[i])
            query += ")"
    query+= " GROUP BY haendelse ORDER BY haendelse;"
    print(query)
    cursor.execute(query)
    return cursor.fetchall()

# queries the database for preceding sensor readings
def get_cluster_sensors(cursor, cluster, interval, sensors):
    start = cluster.date - datetime.timedelta(seconds=interval)
    query = "SELECT " + sensors[0] 
    for i in range(1, len(sensors)):
        query += ", " + sensors[i]
    query += " FROM opkald2 WHERE anlaegid = " + str(cluster.machineID) + " AND opkdato > \"" + str(start) + "\" AND opkdato < \"" + str(cluster.date) + "\" "
    query += " ORDER BY anlaegid;"
    print(query)
    cursor.execute(query)
    return cursor.fetchall()

    
def parse_sensors(sensordata, sensornames):
    values = []
    i = 0
    for sensor in sensornames:
            values.append(parse_value(sensor, sensordata[i]))
            i += 1
    return values

data = pickle.load(open("clusters.rick", "rb"))
sensordata = get_cluster_sensors(cursor, data[0], 1209600, sensornames)
print(sensordata)
for row in sensordata:
    print(parse_sensors(row, sensornames))
print(get_cluster_incidents(cursor, data[0], 1209600))