import mysql.connector as msql
import json
import collections

db= msql.connect(
    host="3.130.126.210",
    port="3309",
    user="pruebas",
    passwd="VGbt3Day5R",
    database="habi_db",
)

cursor = db.cursor()