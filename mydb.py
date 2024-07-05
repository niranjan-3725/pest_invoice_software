import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Password1234'
)

#prepare database cursor
cursorObject = dataBase.cursor()

#Create dataBase

cursorObject.execute("CREATE DATABASE NIRANJAN")

print('All Done!')