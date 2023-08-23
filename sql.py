# Imported Packages
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="root",
  database = "ecommerce"
)
cursor = mydb.cursor()

def select_account(ID):
    global cursor
    acc = {}

    cursor.execute(f"SELECT * from users where id = {ID}")
    result = cursor.fetchall()

    for x in result:
        acc['name'] = x[0]
        acc['password']= x[1]
    return acc
