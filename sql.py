# Imported Packages
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="root"
)

print(mydb)
