import time
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  String, Column, VARCHAR
from sqlalchemy.sql import func
from database import db_session
application = Flask(__name__)
# DB name = orgt_chechoffs
# todo: shouldn't a checkoff belong to a sport or a checkoff sheet?

orgt_member = ""
member_id = 0

application.secret_key = "super secret key"
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/orgt_chechoffs'
db = SQLAlchemy(application)
          
@application.route('/')
def start():
       return render_template('login.html')

@application.route('/', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      orgt_member = request.form['member_name']
      member_id_query = db.engine.execute('SELECT member_id FROM staff_members WHERE name=%s', orgt_member)
      member_id = member_id_query.fetchall()
      # should we add them to the table if they are not already added
      return redirect(url_for('choose_sport', name = orgt_member))
   else:
      # request.method == 'GET'
      # orgt_member = request.args.get('member_name')
      return redirect(url_for('success', name = orgt_member, dumb_var= "dummy :)"))

@application.route('/choose_sport/<name>')
def choose_sport(name):
   sports_query = db.engine.execute('SELECT * FROM sport')
   orgt_sports = sports_query.fetchall()
   return render_template('sports.html', name=name, sports=orgt_sports)

@application.route('/checkoff_sheet/<name>', methods = ['POST'])
def display_checkoff_sheet(name):
   startTime = time.time()
   posQuery = db.engine.execute('SELECT position_name FROM sheet_contains WHERE sheet_name = \'Rock Climbing Checkoff Sheet\'')
   categoryQuery = db.engine.execute('SELECT * FROM category WHERE name = \'Competency and Personal Checkoffs\'')
   checkoffQuery = db.engine.execute('SELECT * FROM checkoff')
   reqsQuery = db.engine.execute('SELECT * FROM requirement ')
   endTime = time.time()

   # use python's 'in list'command to filter the checkoffs by category
   query_execution_time = endTime - startTime
   pos = posQuery.fetchall()
   cat = categoryQuery.fetchall()
   chks = checkoffQuery.fetchall()
   print(chks)
   reqs = reqsQuery.fetchall()
   return render_template('checkoffs.html', 
         name = name,
         categories=cat,
         positions=pos,
         checkoffs=chks,
         requirements=reqs,
         time=query_execution_time) 

@application.route('/checkoff_sheet_complete/<checkoff_id>', methods = ['POST'])
def display_checkoff_sheet_complete(checkoff_id):  
   # find out how to pass name through here
   # todo: find out how to not route if 
      if request.method == 'POST':
         name_member_signing_off = request.form['signing_member_name']
         if (not name_member_signing_off):
            flash("Signature field is empty")
         else:
            db.engine.execute('UPDATE checkoff SET signature = \'%s\', date_time = CURRENT_TIMESTAMP WHERE checkoff_id = %s' % (name_member_signing_off, checkoff_id))
         # display_checkoff_sheet(name)

      return display_checkoff_sheet(orgt_member) 
      # todo: this does NOT change the route name


      # return redirect(url_for('choose_sport', name = orgt_member))

      # startTime = time.time()
      # posQuery = db.engine.execute('SELECT * FROM position WHERE abbreviation = \'IIT\'')
      # categoryQuery = db.engine.execute('SELECT * FROM category WHERE name = \'Competency and Personal Checkoffs\'')
      # checkoffQuery = db.engine.execute('SELECT * FROM checkoff')
      # reqsQuery = db.engine.execute('SELECT * FROM requirement ')
      # endTime = time.time()

      # query_execution_time = endTime - startTime
      # pos = posQuery.fetchall()
      # cat = categoryQuery.fetchall()
      # chks = checkoffQuery.fetchall()
      # reqs = reqsQuery.fetchall()
      # return render_template('checkoffs.html', 
      #       name = name,
      #       categories=cat,
      #       positions=pos,
      #       checkoffs=chks,
      #       requirements=reqs,
      #       time=query_execution_time) 




@application.route('/success/<name><dumb_var>')
def success(name, dumb_var):
   return 'welcome %s, %s' % (name, dumb_var)
if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)      


'''
SELECT requirement.description, requirement.signature, requirement.date_time, checkoff.checkoff_id
FROM requirement
INNER JOIN checkoff
ON requirement.checkoff_id=checkoff.checkoff_id;
'''

# @app.route('/<string:page_name>/')
# def render_static(page_name):
#         return render_template('%s.html' % page_name)</string:page_name>

def playingWithPython():
       return
        # return redirect(url_for('login'))
      #   start = func.current_timestamp()
      #   result = db.engine.execute('SELECT * FROM checkoff_sheet')
      #   end = func.current_timestamp()
      #   names = [row[0] for row in result] # names is a list

      #   str = ""
      #   for name in names:
      #       str += name + "<br>"
      #   return str(end - start)

#     printthis
#     for i in result:
#             printthis += row[i]];
#     return (row[0] for row in result)

