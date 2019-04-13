from flask import Flask, render_template, redirect, url_for, request
from db_handler import *
from logic import *

app = Flask(__name__)

# name of user 'logged in' (no authentication currently)
user = "ADMIN"
# whether or not user logged in is an instructor
is_i = False

@app.route("/")
def start():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def login():
    global user
    global is_i
    if request.method == "POST":
        pname = request.form["member_name"]
        user = pname
        is_i = is_instructor(user)
        return redirect(url_for("choose_sport", name=pname))

@app.route("/choose_sport/<name>")
def choose_sport(name):
    return render_template("sports.html", name=name, sports=["Rock Climbing", "Backpacking", "Bikepacking", "Cascading", "Caving", "Mountain Biking", "Sea Kayaking", "Whitewater Kayaking"])

@app.route("/checkoff_sheet/<name>", methods=["GET", "POST"])
def display_checkoff_sheet(name):
    global is_i
    doc = select_document_checkoff_sheets_collection(id=generate_id(name))
    if is_i:
        return render_template("checkoffs.html", name=name, document=doc)
    else:
        return render_template("checkoffs_view_only.html", name=name, document=doc)

@app.route("/update_checkoffs/<name>", methods=["POST"])
def update_checkoff(name):
    global user
    selected = request.form.getlist("checkbox")
    give_checkoffs(name, selected, user)
    doc = select_document_checkoff_sheets_collection(id=generate_id(name))
    return render_template("checkoffs.html", name=name, document=doc)

if __name__=="__main__":
    app.run()
