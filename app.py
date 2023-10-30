from flask import Flask, templating, redirect, request, session
import pandas as pd
from sql import *
from search import engine


app = Flask(__name__)
app.secret_key = 'root'
app.config['UPLOAD_FOLDER'] = './static/images'

# Home Page


@app.route('/', methods=['GET', 'POST'])
def home():
    products = fetch_category('deals')
    return templating.render_template("home.html",products = products)


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
                return redirect('/account')

    return templating.render_template("signin.html", message=alert_message)

# Sign Out Route


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect('/')


# Create Account Page
@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    alert_message = ""
    if request.method == 'POST':
        match account_creation(request.form['username'],
                               request.form['password']):

            case 'existsError':
                alert_message = 'Sorry, an account with this username already exists. Please use another one.'

            case 'lengthError':
                alert_message = 'This username or password is too long, please shorten it.'

            case 'nullError':
                alert_message = 'Username or password cannot be null, please enter a value'

            case 'success':
                return redirect('/signin')

    return templating.render_template("createaccount.html", message=alert_message)


# Account Page
@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' not in session:
        return redirect('/signin')

    return templating.render_template("account.html", username=session['username'])


# Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        matches = pd.DataFrame()
        try:
            matches = engine(request.form['search'])
            print(matches)
            return templating.render_template("search.html", matches=matches.to_shtml(classes='table table-striped',
                                                                                     index=False))
        except TypeError:
            pass
    return templating.render_template("search.html")


# Category Page
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category(category_name):
    results = fetch_category(category=category_name)
    return templating.render_template("category.html", category=category_name, results=results.to_html(classes='table table-striped',
                                                                                                       index=False, justify='center', render_links=True))


# Product Page
@app.route('/product/<product_name>', methods=['GET', 'POST'])
def product(product_name):
    results = fetch_product(product_name)
    if request.method == 'POST':
        session['orderid'] = request.form['orderid']
    return templating.render_template("product.html", results=results,product_name = product_name,more_products = more_products(results.category))


# Order Page
@app.route('/order', methods=['GET', 'POST'])
def order():
    product = fetch_product(session['orderid'])
    return templating.render_template("order.html",orderid = session['orderid'], product = product)


# Status (For Delivery) Page
@app.route('/status', methods=['GET', 'POST'])
def status():
    if 'username' not in session:
        return redirect('/signin')

    return templating.render_template("status.html")


# Sell Page
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'username' not in session:
        return redirect('/signin')

    if request.method == "POST":
        id = insert_product(
            request.form['itemName'],
            request.form['description'],
            request.form['price'],
            request.form['discount'],
            request.form['stock'],
            request.form['category'],
            session['username']
        )

        f = request.files['image']
        f.save('./static/images/'+str(id)+'.jpg')


    results = fetch_user(session['username'])
    return templating.render_template("sell.html", results=results.to_html(classes='table table-striped',
                                                                           index=False))


if __name__ == "__main__":
    app.run(debug=True)
