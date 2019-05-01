from chpdb import cursor
import pickle
import datetime
from model.misfirecluster import MisfireCluster
from src.parser import parse_value
sensornames = ['actual_rpm']
incidents = [103, 101, 100, 102]

# queries the database for preceding incidents
def get_cluster_incidents(date, machineID, interval, haendelser = []):
    start = date - datetime.timedelta(seconds=interval)
    query = "SELECT haendelse, COUNT(*) FROM anlaegshaendelser " \
            " WHERE anlaeg_id = " + str(machineID) + " AND dato < \"" + str(date) + "\" AND " \
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
def get_cluster_sensors(date, machineID, interval, sensors):
    start = date - datetime.timedelta(seconds=interval)
    query = "SELECT " + sensors[0] 
    for i in range(1, len(sensors)):
        query += ", " + sensors[i]
    query += " FROM opkald2 WHERE anlaegid = " + str(machineID) + " AND opkdato > \"" + str(start) + "\" AND opkdato < \"" + str(date) + "\" "
    query += " ORDER BY anlaegid;"
    print(query)
    cursor.execute(query)
    return cursor.fetchall()

#Returns true if there is a misfire
def check_for_future_misfire(date, machineID, interval):
    cursor.execute("SELECT opkdato FROM anlaegshaendelser WHERE haendelse = 112 AND misfire_shutdown = 1 AND opkdato > \"" + str(date) + "\" AND opkdato < \"" + str(date + interval) "\" ")
    return cursor.fetchall() != []
    
def parse_sensors(sensordata, sensornames):
    values = []
    i = 0
    for sensor in sensornames:
            values.append(parse_value(sensor, sensordata[i]))
            i += 1
    return values

