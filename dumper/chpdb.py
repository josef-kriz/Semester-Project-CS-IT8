import mysql.connector

mydb = mysql.connector.connect(
    host="192.38.56.161",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)

cursor = mydb.cursor()
