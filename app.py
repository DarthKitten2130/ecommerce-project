from flask import Flask,templating
from sql import *


app = Flask(__name__)

# Home Page
@app.route('/', methods = ['GET','POST'])
def home():
   return templating.render_template("home.html")

# Account Page
@app.route('/account',methods = ['GET','POST'])
def account():
   return templating.render_template("account.html")

# Search Page
@app.route('/search',methods = ['GET','POST'])
def search():
   return templating.render_template("search.html")

# Categories Page
@app.route('/categories',methods = ['GET','POST'])
def categories():
   return templating.render_template("categories.html")

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
   return templating.render_template("status.html")

# Sell Page
@app.route('/sell',methods = ['GET','POST'])
def sell():
   return templating.render_template("sell.html")


if __name__ =="__main__":  
    app.run(debug = True)
