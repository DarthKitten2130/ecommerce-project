import mysql.connector as mysql
import pandas as pd

mydb = mysql.connect(host = 'localhost',username = 'root', password = 'root', database = 'ecommerce')
cursor = mydb.cursor()
def engine(phrase):
    global cursor
    
    cursor.execute("select name from products")
    output = cursor.fetchall()
    
    for name in output:
        pass
        
        
engine("Hi")