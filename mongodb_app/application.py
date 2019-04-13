from flask import Flask, render_template, redirect, url_for, request
from db_handler import *
from logic import *

# initialize flask app
app = Flask(__name__)

# name of user 'logged in' (no authentication currently)
user = ""


@app.route("/")
def start():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def login():
    global user
    if request.method == "POST":
        pname = request.form["member_name"]
        user = pname
        return redirect(url_for("choose_sport", name=pname))

@app.route("/choose_sport/<name>")
def choose_sport(name):
    global user
    view = ""
    if is_tl(user):
        view = "sports_tl_view.html"
    elif is_instructor(user):
        view = "sports_instructor_view.html"
    else:
        view = "sports.html"
    return render_template(view, name=name, sports=["Rock Climbing", "Backpacking", "Bikepacking", "Cascading", "Caving", "Mountain Biking", "Sea Kayaking", "Whitewater Kayaking"])

@app.route("/checkoff_sheet/<name>", methods=["GET", "POST"])
def display_checkoff_sheet(name):
    doc = select_document_checkoff_sheets_collection(id=generate_id(name))
    return render_template("checkoffs_view_only.html", name=name, document=doc)

@app.route("/update_checkoffs/<name>", methods=["POST"])
def update_checkoff(name):
    global user
    selected = request.form.getlist("checkbox")
    give_checkoffs(name, selected, user)
    doc = select_document_checkoff_sheets_collection(id=generate_id(name))
    return render_template("checkoffs.html", name=name, document=doc)

@app.route("/search_staff", methods=["POST"])
def search_staff():
    search_name = request.form["search_name"]
    doc = select_document_checkoff_sheets_collection(id=generate_id(search_name))
    return render_template("checkoffs.html", name=search_name, document=doc)

@app.route("/add_checkoff", methods=["POST"])
def add_checkoff():
    cat_name = request.form["category"]
    check_name = request.form["checkoff_name"]
    new_req_description = request.form["req_description"]
    add_requirement(cat_name, check_name, new_req_description)
    return render_template("sports_tl_view.html", name=user, sports=["Rock Climbing", "Backpacking", "Bikepacking", "Cascading", "Caving", "Mountain Biking", "Sea Kayaking", "Whitewater Kayaking"])

# run Flask app automatically
if __name__=="__main__":
    app.run()
