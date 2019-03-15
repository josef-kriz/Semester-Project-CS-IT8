import mysql.connector
import json
import pickle
from model.entry import Entry

def save_dump(data, path):
    f = open(path, "wb")
    pickle.dump(data, f)
    f.close()

columns = ['husets_elforbrug', 'antennesignal']

mydb = mysql.connector.connect(
    host="localhost",
    user="python",
    passwd="python",
    database="csit8"
)

my_cursor = mydb.cursor()

my_cursor.execute('SELECT opkdato, ' + ' '.join(columns) + ' FROM opkald2 WHERE anlaegId = 2000799148 ORDER BY opkdato ASC')

result = my_cursor.fetchall()

array = []
for res in result:
    date = res[0]
    values = dict()
    i = 0
    for column in columns:
        values[column] = res[1]
    array.append(Entry(date, values))

save_dump(array, 'data/2000799148_husets')





