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
        acc['id'] = x[0]
        acc['fname'] = x[1]
        acc['lname'] = x[2]
        acc['address'] = x[3]
        acc['zip']= x[4]
        acc['password']= x[5]
    return acc

print(select_account(0))
