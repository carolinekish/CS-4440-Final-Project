import time
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  String, Column, VARCHAR
from sqlalchemy.sql import func
application = Flask(__name__)
# DB name = orgt_chechoffs
# todo: shouldn't a checkoff belong to a sport or a checkoff sheet?

# THIS IS THE LOGGED IN USER:
member_name = ""
member_id = 0 # 0 is not a valid member_id
member_position_title = ""

# THIS IS THE STAFF MEMBER THE LOGGED IN USER SEARCHED FOR:
searched_member_name = ""
searched_member_id = 0

application.secret_key = "super secret key"
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/orgt_chechoffs'
db = SQLAlchemy(application)

def getCorrectCategories(positions):
   positionValues = "("
   for position in positions:
      positionValues += '\'' + position.position_name + '\','
   positionValues = positionValues[:-1]
   positionValues += ')'
   pos_query_string = 'SELECT * FROM belongs_to WHERE pos_name in ' + positionValues
   return pos_query_string

def getCompletedCheckoffIDs(completed_checkoffs):
   completed_ids = []
   for checkoff in completed_checkoffs:
      completed_ids.append(checkoff.checkoff)
   return completed_ids

def getCompletedRequirementIDs(completed_reqs):
    completed_ids = []
    for req in completed_reqs:
        completed_ids.append(req.req_id)
    return completed_ids

@application.route('/')
def start():
       return render_template('login.html')

@application.route('/', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      orgt_member = request.form['member_name']
      member_id_query = db.engine.execute('SELECT * FROM staff_members WHERE name=%s', orgt_member)
      result = member_id_query.first()
      if result != [] :
         global member_id # needed in order to MODIFY a global variable
         global member_name
         global member_position_title
         member_id = result[0] # should we add them to the table if they are not already added
         member_name = result[1]
         member_position_title = result[2]
         return redirect(url_for('choose_sport', name = member_name))
      else:
         print('Something went wrong with login')

@application.route('/choose_sport/<name>')
def choose_sport(name):
   sports_query = db.engine.execute('SELECT * FROM sport')
   orgt_sports = sports_query.fetchall()
   return render_template('sports.html', name=name, sports=orgt_sports, position=member_position_title)

@application.route('/checkoff_sheet_user', methods=["POST"])
def show_own_checkoffs():
   return redirect(url_for('display_checkoff_sheet', name = member_name, member_id = member_id))

@application.route("/search_staff", methods=["POST"])
def search_staff():
   search_name = request.form["search_name"]
   query = db.engine.execute('SELECT * FROM staff_members WHERE name=%s',search_name)
   found_member = query.first()
   if found_member != [] :
      global searched_member_id
      global searched_member_name
      searched_member_id = found_member[0]
      searched_member_name = found_member[1]
      return redirect(url_for('display_checkoff_sheet', name = searched_member_name, member_id = searched_member_id))
    
@application.route("/add_requirement", methods=["POST"])
def add_requirement():
   # sport = request.form["sport"]
   # position = request.form["position"]
   # category = request.form["category"]
   checkoff = request.form["checkoff"]
   req_description= request.form["req_description"]

   checkoff_query = db.engine.execute('SELECT checkoff_id FROM checkoff WHERE title=%s', checkoff)
   checkoff_id = checkoff_query.first()[0]
   startTime = time.time()
   db.engine.execute('INSERT INTO requirement (description, checkoff_id) VALUES (%s,%s)', req_description, checkoff_id)
   endtime = time.time()
   print("total insert time: %f " %(endtime -startTime))
   return redirect(url_for('choose_sport', name = member_name))
    
@application.route('/checkoff_sheet/<name>_<member_id>', methods = ['GET', 'POST'])
def display_checkoff_sheet(name, member_id):

    startTime = time.time() # start time

    posQuery = db.engine.execute('SELECT position_name FROM sheet_contains WHERE sheet_name = \'Rock Climbing Checkoff Sheet\'') # todo: paramaterize the sport?
    positions = posQuery.fetchall()
    category_query_string = getCorrectCategories(positions)
    cat_belongsTo_position_Query = db.engine.execute(category_query_string)
    checkoffQuery = db.engine.execute('SELECT * FROM checkoff')
    startJoin = time.time()
    reqsQuery = db.engine.execute('SELECT checkoff.checkoff_id, requirement.req_id, requirement.description FROM requirement INNER JOIN checkoff ON requirement.checkoff_id=checkoff.checkoff_id')
    endJoin = time.time()
    completedCheckoffsQuery = db.engine.execute('SELECT checkoff, signature, date_time FROM completed_checkoffs WHERE member=%s', member_id)
    completedReqsQuery = db.engine.execute('SELECT * FROM completed_requirements WHERE member=%s', member_id)

    endTime = time.time() # end time
    query_execution_time = endTime - startTime

    cat = cat_belongsTo_position_Query.fetchall()
    chks = checkoffQuery.fetchall()
    completed_chks = completedCheckoffsQuery.fetchall()
    completed_ids = getCompletedCheckoffIDs(completed_chks)
    reqs = reqsQuery.fetchall()
    completed_reqs = completedReqsQuery.fetchall()
    completed_req_ids = getCompletedRequirementIDs(completed_reqs)

    print("join time: %f" %(endJoin - startJoin))

    view = ''
    if name == member_name and member_id == member_id :
      view = 'checkoffs_view_only.html'
    else:
      view = 'checkoffs.html'

    return render_template(view,
            name = name,
            categories=cat,
            positions=positions,
            checkoffs=chks,
            requirements=reqs,
            completed_ids=completed_ids,
            completed_checkoffs=completed_chks,
            completed_reqs=completed_req_ids,
            time=query_execution_time)

@application.route('/requirement_confirm/<checkoff_id>', methods = ['POST'])
def display_requirement_confirmation(checkoff_id):

    reqIdQuery = db.engine.execute('SELECT req_id FROM requirement WHERE checkoff_id = %s', checkoff_id)
    reqIds = reqIdQuery.fetchall()
    reqIdList = []
    for id in reqIds:
        reqIdList.append(id.req_id)
    completed_reqs = []
    startTime = time.time()
    for id in reqIdList:
        name = 'checkbox' + str(id)
        try:
            value = request.form[name]
            completed_reqs.append(id)
            try:
                db.engine.execute(
                    'INSERT INTO completed_requirements (member, req_id, signature, date_time) VALUES (%s,%s,%s,CURRENT_TIMESTAMP)',
                    searched_member_id, id, member_name)
            except:
                print("Already Completed!")

        except KeyError:
            print("bad key: ", name)

    endTime = time.time()
    query_execution_time = endTime-startTime
    return render_template('req_confirm.html',
                           chk_id=checkoff_id,
                           memberid=member_id,
                           searched_member_name=searched_member_name,
                           searched_member_id=searched_member_id,
                           completed_reqs=completed_reqs,
                           time=query_execution_time)

@application.route('/checkoff_confirm/<checkoff_id>', methods = ['POST'])
def display_checkoff_confirmation(checkoff_id):
   startTime = time.time()
   db.engine.execute(
        'INSERT INTO completed_checkoffs (member, checkoff, signature, date_time) VALUES (%s,%s,%s,CURRENT_TIMESTAMP)',
        searched_member_id, checkoff_id, member_name)
   endtime = time.time()
   query_execution_time = endtime-startTime
   return render_template('checkoff_confirm.html',
                           chk_id=checkoff_id,
                           memberid=member_id,
                           searched_member_name=searched_member_name,
                           searched_member_id=searched_member_id,
                           time=query_execution_time)

if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)
