import mysql.connector

mydb = mysql.connector.connect(
    host="192.38.56.161",
    user="chp",
    passwd="<password>",
    database="ecpower"
)

cursor = mydb.cursor()
