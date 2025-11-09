# Imported Packages
import random
import mysql.connector
import pandas as pd
from classes import Product
import os

# MySQL Configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'ecommerce'),
    'autocommit': False
}

mysqlConnection = mysql.connector.connect(**db_config)
cursor = mysqlConnection.cursor()

# Account Functions


def create_table():
    # Create database if it doesn't exist (handled at connection level)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            address TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            price DECIMAL(10,2),
            discount DECIMAL(3,2),
            stock INT,
            category VARCHAR(100),
            seller VARCHAR(255),
            sold INT DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credit_card (
            number VARCHAR(20) PRIMARY KEY, 
            cvv VARCHAR(4),
            username VARCHAR(255)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user VARCHAR(255),
            product VARCHAR(255),
            buy_date DATE
        )
    ''')

    # MySQL Triggers
    # Trigger 1: Prevent negative stock
    cursor.execute('DROP TRIGGER IF EXISTS prevent_negative_stock')
    cursor.execute('''
        CREATE TRIGGER prevent_negative_stock
        BEFORE UPDATE ON products
        FOR EACH ROW
        BEGIN
            IF NEW.stock < 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Stock cannot be negative';
            END IF;
        END
    ''')

    # Trigger 2: Auto-lowercase usernames for consistency
    cursor.execute('DROP TRIGGER IF EXISTS lowercase_username')
    cursor.execute('''
        CREATE TRIGGER lowercase_username
        BEFORE INSERT ON users
        FOR EACH ROW
        BEGIN
            IF NEW.username != LOWER(NEW.username) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Username must be lowercase';
            END IF;
        END
    ''')

    # Trigger 3: Validate discount range (must be between 0 and 1)
    cursor.execute('DROP TRIGGER IF EXISTS validate_discount')
    cursor.execute('''
        CREATE TRIGGER validate_discount
        BEFORE INSERT ON products
        FOR EACH ROW
        BEGIN
            IF NEW.discount < 0 OR NEW.discount > 1 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Discount must be between 0 and 1';
            END IF;
        END
    ''')

    # Also validate discount on updates
    cursor.execute('DROP TRIGGER IF EXISTS validate_discount_update')
    cursor.execute('''
        CREATE TRIGGER validate_discount_update
        BEFORE UPDATE ON products
        FOR EACH ROW
        BEGIN
            IF NEW.discount < 0 OR NEW.discount > 1 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Discount must be between 0 and 1';
            END IF;
        END
    ''')

    # MySQL Stored Procedures
    # Procedure 1: Get user statistics (total products sold, revenue, etc.)
    cursor.execute('DROP PROCEDURE IF EXISTS get_seller_stats')
    cursor.execute('''
        CREATE PROCEDURE get_seller_stats(IN seller_name VARCHAR(255))
        BEGIN
            SELECT 
                seller_name as seller,
                COUNT(*) as total_products,
                SUM(sold) as total_items_sold,
                SUM(sold * price * (1 - discount)) as total_revenue,
                AVG(price * (1 - discount)) as avg_product_price
            FROM products
            WHERE seller = seller_name
            GROUP BY seller;
        END
    ''')

    # Procedure 2: Update product discount
    cursor.execute('DROP PROCEDURE IF EXISTS update_product_discount')
    cursor.execute('''
        CREATE PROCEDURE update_product_discount(
            IN product_id VARCHAR(255),
            IN new_discount DECIMAL(3,2)
        )
        BEGIN
            IF new_discount < 0 OR new_discount > 1 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Discount must be between 0 and 1';
            ELSE
                UPDATE products 
                SET discount = new_discount 
                WHERE id = product_id;
            END IF;
        END
    ''')

    # Procedure 3: Get low stock products
    cursor.execute('DROP PROCEDURE IF EXISTS get_low_stock_products')
    cursor.execute('''
        CREATE PROCEDURE get_low_stock_products(IN threshold INT)
        BEGIN
            SELECT id, name, stock, seller, category
            FROM products
            WHERE stock <= threshold AND stock > 0
            ORDER BY stock ASC;
        END
    ''')

    # Procedure 4: Get top selling products
    cursor.execute('DROP PROCEDURE IF EXISTS get_top_selling_products')
    cursor.execute('''
        CREATE PROCEDURE get_top_selling_products(IN limit_count INT)
        BEGIN
            SELECT 
                id, 
                name, 
                description, 
                price, 
                discount, 
                sold,
                (price * (1 - discount)) as discounted_price,
                (sold * price * (1 - discount)) as total_revenue
            FROM products
            WHERE sold > 0
            ORDER BY sold DESC
            LIMIT limit_count;
        END
    ''')

    # Procedure 5: Process order (combines stock update and order history)
    cursor.execute('DROP PROCEDURE IF EXISTS process_order')
    cursor.execute('''
        CREATE PROCEDURE process_order(
            IN p_username VARCHAR(255),
            IN p_product_id VARCHAR(255)
        )
        BEGIN
            DECLARE current_stock INT;
            
            -- Check stock availability
            SELECT stock INTO current_stock 
            FROM products 
            WHERE id = p_product_id;
            
            IF current_stock IS NULL THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Product not found';
            ELSEIF current_stock <= 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Product out of stock';
            ELSE
                -- Update stock and sold count
                UPDATE products 
                SET stock = stock - 1, sold = sold + 1 
                WHERE id = p_product_id;
                
                -- Insert into order history
                INSERT INTO order_history (user, product, buy_date) 
                VALUES (p_username, p_product_id, CURDATE());
            END IF;
        END
    ''')

    mysqlConnection.commit()


def account_verification(username, password):
    global cursor
    cursor.execute(
        'SELECT username, password FROM users WHERE username = %s', (username,))
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
    cursor.execute('SELECT username FROM users')
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
        cursor.execute(
            'INSERT INTO users VALUES(%s, %s, NULL)', (username, password))
        mysqlConnection.commit()
        return 'success'


# Product Functions
def engine(phrase):
    phrase = phrase.lower()
    cursor.execute(
        'SELECT id, name, description, price, discount, stock, category, seller, CONCAT("http://127.0.0.1:5000/product/", id) as link FROM products')
    output = cursor.fetchall()

    df = pd.DataFrame(columns=['name', 'description',
                      'price', 'discount', 'discounted price', 'link'])

    for x in output:
        product = Product(
            x[0],
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
            x[6],
            x[7])

        if phrase in product.name.lower():
            df.loc[len(df)] = [product.name,
                               product.description,
                               product.price,
                               product.discount,
                               product.discounted_price,
                               x[8]
                               ]

    return df


def insert_product(name, description, price, discount, stock, category, seller):
    global cursor

    cursor.execute('SELECT id FROM products')
    output = cursor.fetchall()

    ids = [x[0] for x in output]

    id = 0

    id = str(random.randrange(0, 999))

    cursor.execute(
        'INSERT INTO products VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0)',
        (id, name, description, price, int(discount)/100, stock, category, seller))
    mysqlConnection.commit()

    return id


def insert_cc(username, number, cvv):
    global cursor

    cursor.execute(
        'INSERT INTO credit_card VALUES(%s, %s, %s)', (number, cvv, username))
    mysqlConnection.commit()


def fetch_product(id):
    global cursor

    cursor.execute("SELECT * FROM products WHERE id = %s AND stock > 0", (id,))
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
        cursor.execute('''SELECT name, description, price, ((1-discount)*price) as discounted, 
            CONCAT("http://127.0.0.1:5000/product/", id) as link FROM products WHERE discount > 0 AND stock > 0''')
        results = cursor.fetchall()
        output = pd.DataFrame(
            results, columns=['name', 'description', 'price', 'discounted price', 'links'])

    elif category == 'home':
        cursor.execute('''SELECT id, name, description, price, ((1-discount)*price) as discounted, 
            CONCAT("http://127.0.0.1:5000/product/", id) as link FROM products WHERE stock > 0''')
        results = cursor.fetchall()
        output = pd.DataFrame(
            results, columns=['id', 'name', 'description', 'price', 'discounted price', 'links'])
        output['id'] = output['id'].astype('str')
    else:
        cursor.execute('''SELECT name, description, price, ((1-discount)*price) as discounted,
                       CONCAT("http://127.0.0.1:5000/product/", id) as link FROM products WHERE category = %s AND stock > 0''', (category,))
        results = cursor.fetchall()
        output = pd.DataFrame(
            results, columns=['name', 'description', 'price', 'discounted price', 'links'])

    return output


def fetch_user(username):
    global cursor

    cursor.execute(
        'SELECT name, description, price, discount, stock FROM products WHERE seller = %s AND stock > 0', (username,))

    results = cursor.fetchall()

    output = pd.DataFrame(
        results, columns=['name', 'description', 'price', 'discount', 'stock'])

    return output


def fetch_cc(username):
    global cursor

    cursor.execute(
        'SELECT number FROM credit_card WHERE username = %s', (username,))

    results = cursor.fetchall()

    return results


def fetch_cvv(cc):
    global cursor

    cursor.execute('SELECT cvv FROM credit_card WHERE number = %s', (cc,))

    results = cursor.fetchall()[0][0]

    return results


def fetch_address(username):
    global cursor

    cursor.execute('SELECT address FROM users WHERE username = %s', (username,))

    results = cursor.fetchall()[0][0]

    return results


def update_stock(username, productid):

    global cursor

    cursor.execute(
        'UPDATE products SET stock = stock - 1 WHERE id = %s', (productid,))
    mysqlConnection.commit()
    cursor.execute(
        'UPDATE products SET sold = sold + 1 WHERE id = %s', (productid,))
    mysqlConnection.commit()
    cursor.execute(
        'INSERT INTO order_history (user, product, buy_date) VALUES(%s, %s, CURDATE())', (username, productid))
    mysqlConnection.commit()


def more_products(category):

    global cursor

    cursor.execute('''SELECT name, description, price, ((1-discount)*price) as discounted,
                       CONCAT("http://127.0.0.1:5000/product/", id) as link, id FROM products WHERE category = %s AND stock > 0''', (category,))

    results = cursor.fetchall()

    return results


def order_history(username):
    global cursor

    cursor.execute('''SELECT name, description, category, seller, ((1-discount)*price) as discounted, buy_date FROM order_history, products 
                   WHERE order_history.user = %s AND order_history.product = products.id''', (username,))

    output = pd.DataFrame(cursor.fetchall(), columns=[
                          'Name', 'Description', 'Category', 'Seller', 'Price', 'Date Bought'])

    return output
