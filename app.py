from flask import Flask, request, render_template, url_for
from main import web_scrapper
from flask_cors import cross_origin
import pickle


# creating Flask Object
app = Flask(__name__)
app.secret_key ="Rupee"




@app.route("/")
@cross_origin()
def home():
    data= web_scrapper("poco m2 pro",4)
    return render_template("results.html",data=data,mobile_name="POCO M2 PRO")
    # return render_template("Main.html")


app.run(debug = True)