from django.test import TestCase
import mysql.connector

# Create your tests here.
checkDB = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rcabralf176@',
    database='geps'
)
cursor = checkDB.cursor()
cursor.execute("SHOW TABLES")
resultado = cursor.fetchone()
if resultado:
    print("OK")
else:
    print("NAO OK")