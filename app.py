from flask import Flask,templating,session
from sql import *


app = Flask(__name__)

# Home Page
@app.route('/', methods = ['GET','POST'])
def home():
   return templating.render_template("home.html")

# Account Page
@app.route('/account',methods = ['GET','POST'])
def account():
   if 'username' in session:
      return templating.render_template("account.html")
   else:
      return templating.render_template('signin.html')

# Search Page
@app.route('/search',methods = ['GET','POST'])
def search():
   return templating.render_template("search.html")

# Categories Page
@app.route('/categories',methods = ['GET','POST'])
def categories():
   return templating.render_template("categories.html")

#Category Page
@app.route('/category/<category_name>',methods = ['GET','POST'])
def category():
   return templating.render_template("category.html")

# Product Page
@app.route('/search/<product_name>',methods = ['GET','POST'])
def product():
   return templating.render_template("product.html")

# Order Page
@app.route('/order',methods = ['GET','POST'])
def order():
   return templating.render_template("order.html")

# Status (For Delivery) Page
@app.route('/status',methods = ['GET','POST'])
def status():
   if 'username' in session:
      return templating.render_template("status.html")
   else:
      return templating.render_template('signin.html')
# Sell Page
@app.route('/sell',methods = ['GET','POST'])
def sell():
   if 'username' in session:
      return templating.render_template("account.html")
   else:
      return templating.render_template('sell.html')

if __name__ =="__main__":  
    app.run(debug = True)
