# Imported Packages
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="root",
  database = "ecommerce"
)
cursor = mydb.cursor()

def account_verification(username,password):
    global cursor
    cursor.execute(f"SELECT username,password from users where username = {username}")
    results = cursor.fetchall()
    acc = {}
    for result in results:
        acc[result[0]] = result[1]

    # Account Does Not Exist
    if username not in [x[0] for x in results]:
        return 'doesNotExist'
    
    # Entered the Wrong Password
    elif acc[username] != password:
        return 'wrongPassword'
    
    # Verified
    elif acc[username] == password:
        return 'verified'