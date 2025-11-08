from flask import Flask, render_template, redirect, request, session
import pandas as pd
from sql import *
import os

app = Flask(__name__)
app.secret_key = 'root'
app.config['UPLOAD_FOLDER'] = './static/images'

# Home Page


@app.route('/', methods=['GET', 'POST'])
def home():
    create_table()
    products = fetch_category('home')
    return render_template("home.html", products=products)


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
                return redirect('/account')

    return render_template("signin.html", message=alert_message)


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

    return render_template("createaccount.html", message=alert_message)


# Account Page
@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' not in session:
        return redirect('/signin')

    products = fetch_user(session['username'])
    if products is None:
        products = pd.DataFrame()
    address = fetch_address(session['username'])
    oh = order_history(session['username'])
    if oh is None:
        oh = pd.DataFrame()

    buser = 'Yes' if len(products) > 0 else 'No'

    if request.method == 'POST':
        insert_cc(session['username'],
                  request.form['card'], request.form['cvv'])

    return render_template(
        "account.html",
        username=session['username'],
        products=products.to_html(classes='table table-striped', index=False),
        address=address,
        buser=buser,
        oh=oh.to_html(classes='table table-striped', index=False)
    )


# Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        matches = engine(request.form['search'])
        if matches is None:
            matches = pd.DataFrame()
        return render_template(
            "search.html",
            matches=matches.to_html(
                classes='table table-striped', index=False, render_links=True)
        )
    return render_template("search.html")


# Category Page
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category(category_name):
    results = fetch_category(category=category_name)
    if results is None:
        results = pd.DataFrame()
    return render_template(
        "category.html",
        category=category_name,
        results=results.to_html(
            classes='table table-striped', index=False, justify='center', render_links=True)
    )


# Product Page
@app.route('/product/<product_name>', methods=['GET', 'POST'])
def product(product_name):
    results = fetch_product(product_name)

    if request.method == 'POST':
        session['orderid'] = request.form['orderid']

    # Access category from Product object
    category_name = results.category

    return render_template(
        "product.html",
        results=results,
        product_name=product_name,
        more_products=more_products(category_name)
    )


# Order Page
@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' not in session:
        return redirect('/signin')

    product = fetch_product(session.get('orderid'))
    address = fetch_address(session['username'])
    cc = fetch_cc(session['username'])
    alert_message = ""

    if request.method == 'POST':
        if request.form['cvv'] == fetch_cvv(request.form['card']):
            update_stock(session['username'], session['orderid'])
        else:
            alert_message = 'Sorry, that is the wrong CVV for this credit card'

    return render_template(
        "order.html",
        orderid=session.get('orderid'),
        product=product,
        cc=cc,
        address=address,
        alert_message=alert_message
    )


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
        filename = f"{id}.jpg"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    results = fetch_user(session['username'])
    if results is None:
        results = pd.DataFrame()

    return render_template(
        "sell.html",
        results=results.to_html(classes='table table-striped', index=False)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
