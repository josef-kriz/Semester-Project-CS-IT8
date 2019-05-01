import pandas as pd
from datetime import datetime
import mysql.connector


def TagMisfires(cursor):
    csv = pd.read_csv('/home/pheaton/Documents/CHP/haendelser_all2.csv')
    length = len(csv['dato'])

    haendelse = 112
    haendelse2 = 81
    time_interval = 7200 #seconds

    for i in range(length-1):
        if i % 30000 == 0:
            print(str((i/length)*100) + '%')

        date1 = datetime.strptime(csv['dato'][i], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(csv['dato'][i+1], '%Y-%m-%d %H:%M:%S')

        if csv['haendelse'][i] == haendelse \
                and (date2 - date1).seconds > time_interval \
                and csv['haendelse'][i+1] == haendelse2 \
                and csv['anlaeg_id'][i] == csv['anlaeg_id'][i+1]:
            cursor.execute('UPDATE anlaegshaendelser SET misfire_shutdown=1 WHERE dato="' + str(csv['dato'][i]) + '" AND anlaeg_id=' + str(csv['anlaeg_id'][i]))

mydb = mysql.connector.connect(
    host="192.38.56.161",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)

mydb.autocommit = True

TagMisfires(mydb.cursor())
