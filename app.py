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
    return render_template("Main.html")

@app.route("/fetch", methods=["POST","GET"])
@cross_origin()
def fetch():
    samp_dict=request.form
    name = samp_dict['m_name']
    count=int(samp_dict["count"])
    data= web_scrapper(name,count)
    return render_template("results.html",data=data,mobile_name=name)

port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host='127.0.0.1', port=port)