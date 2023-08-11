from flask import Flask,templating


app = Flask(__name__)

# Home Page
@app.route('/', methods = ['GET','POST'])
def home():
   return templating.render_template("home.html")
   