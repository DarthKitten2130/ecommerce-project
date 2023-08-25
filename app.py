from flask import Flask, templating, session, redirect,request
from sql import *


app = Flask(__name__)
app.secret_key= 'root'

# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    return templating.render_template("home.html")


# Sign in Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
   alert_message = ""
   if request.method == 'POST':
        match account_verification(request.form['username'],
                                   request.form['password']):
            
            case 'doesNotExist':
                alert_message = "Sorry, your account does not exist, please create one." 
            
            case 'wrongPassword':
                alert_message = "The password you entered is incorrect, please try again."
                
            case 'verified':
               session['username'] = request.form['username']
               session['password'] = request.form['password']        
               return redirect('/')
            
   return templating.render_template("signin.html", message = alert_message)
            
    
# Account Page
@app.route('/account', methods=['GET', 'POST'])
def account():
    while 'username' not in session:
        return redirect('/signin')

    return templating.render_template("account.html")


# Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    return templating.render_template("search.html")


# Categories Page
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    return templating.render_template("categories.html")


# Category Page
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category():
    return templating.render_template("category.html")


# Product Page
@app.route('/search/<product_name>', methods=['GET', 'POST'])
def product():
    return templating.render_template("product.html")


# Order Page
@app.route('/order', methods=['GET', 'POST'])
def order():
    return templating.render_template("order.html")


# Status (For Delivery) Page
@app.route('/status', methods=['GET', 'POST'])
def status():
    while 'username' not in session:
        return redirect('/signin')

    return templating.render_template("status.html")


# Sell Page
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    while 'username' not in session:
        return redirect('/signin')

    return templating.render_template("sell.html")


if __name__ == "__main__":
    app.run(debug=True)
