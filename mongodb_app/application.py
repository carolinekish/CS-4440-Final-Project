from flask import Flask, render_template, redirect, url_for, request
from db_handler import *
from logic import *

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("login.html")

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        pname = request.form["member_name"]
        return redirect(url_for("choose_sport", name=pname))

@app.route("/choose_sport/<name>")
def choose_sport(name):
    return render_template("sports.html", name=name, sports=["Rock Climbing", "Backpacking", "Bikepacking", "Cascading", "Caving", "Mountain Biking", "Sea Kayaking", "Whitewater Kayaking"])

@app.route("/checkoff_sheet/<name>", methods=["POST"])
def display_checkoff_sheet(name):
    doc = select_document_checkoff_sheets_collection(id=generate_id(name))
    return render_template("checkoffs.html", document=doc)

if __name__=="__main__":
    app.run()
