# Imported Packages
import random
import mysql.connector as mysql
import pandas as pd
from classes import Product

mydb = mysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce"
)
cursor = mydb.cursor()

# Account Functions


def account_verification(username, password):
    global cursor
    cursor.execute(
        f'SELECT username,password from users where username = "{username}"')
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


def account_creation(username, password):
    global cursor
    cursor.execute('Select username from users')
    results = cursor.fetchall()
    usernames = [x[0] for x in results]

    # Account Exists
    if username in usernames:
        return 'existsError'

    # Too Long
    elif len(username) > 255 or len(password) > 255:
        return 'lengthError'

    # Too Short
    elif len(username) == 0 or len(password) == 0:
        return 'nullError'

    # Success
    else:
        cursor.execute(f'insert into users values("{username}","{password}")')
        cursor.execute('commit')
        return 'success'


# Product Functions
def fetch_product(id):
    global cursor

    cursor.execute(f"Select * from products where id = {id}")
    results = cursor.fetchall()
    x = results[0]

    product = Product(
        x[0],
        x[1],
        x[2],
        x[3],
        x[4],
        x[5],
        x[6],
        x[7])

    return product


def fetch_category(category):
    global cursor

    if category == 'deals':
        cursor.execute(f'''Select name,description,price,((1-discount)*price) as discounted, 
            concat("http://127.0.0.1:5000/product/",id) as link from products where discount > 0''')
        results = cursor.fetchall()
        output = pd.DataFrame(
        results, columns=['name', 'description', 'price', 'discounted price', 'links'])
    
    elif category == 'home':
        cursor.execute(f'''Select id,name,description,price,((1-discount)*price) as discounted, 
            concat("http://127.0.0.1:5000/product/",id) as link from products where discount > 0''')
        results = cursor.fetchall()
        output = pd.DataFrame(
        results, columns=['id','name', 'description', 'price', 'discounted price', 'links'])
        output['id']= output['id'].astype('str')
    else:
        cursor.execute(f'''Select name,description,price,((1-discount)*price) as discounted,
                       concat("http://127.0.0.1:5000/product/",id) as link from products where category = "{category}"''')
        results = cursor.fetchall()
        output = pd.DataFrame(
        results, columns=['name', 'description', 'price', 'discounted price', 'links'])

    

    return output


def fetch_user(username):
    global cursor

    cursor.execute(
        f'Select name,description,price,discount,stock from products where seller = "{username}"')

    results = cursor.fetchall()

    output = pd.DataFrame(
        results, columns=['name', 'description', 'price', 'discount','stock'])

    return output


def insert_product(name, description, price, discount, stock, category, seller):
    global cursor

    cursor.execute('select id from products')
    output = cursor.fetchall()

    ids = [x[0] for x in output]

    id = 0

    while id in ids:
        id = (random.randrange(0, 999))

    cursor.execute(f'insert into products values({id},"{name}","{description}",{price},{int(discount)/100},{stock},"{category}","{seller}")')
    cursor.execute('commit')

    return id


def more_products(category):

    global cursor

    cursor.execute(f'''Select name,description,price,((1-discount)*price) as discounted,
                       concat("http://127.0.0.1:5000/product/",id) as link,id from products where category = "{category}"''')

    results = cursor.fetchall()

    return results


def fetch_cc(username):
    global cursor

    cursor.execute(f'select number from credit_card where username = "{username}"')

    results = cursor.fetchall()

    return results


def fetch_address(username):
    global cursor
    
    cursor.execute(f'select address from users where username = "{username}"')
    
    results = cursor.fetchall()[0][0]
    
    return results


def fetch_cvv(cc):
    global cursor
    
    cursor.execute(f'select cvv from credit_card where number = {cc}')
    
    results = cursor.fetchall()[0][0]
    
    return results


def update_stock(productid):
    
    global cursor

    cursor.execute(f'update products set stock = stock - 1 where id = {productid}')
    cursor.execute(f'update products set sold = sold + 1 where id = {productid}')
    cursor.execute('commit')