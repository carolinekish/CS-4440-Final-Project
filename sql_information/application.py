from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  String, Column, VARCHAR
from sqlalchemy.sql import func
application = Flask(__name__)
# USE orgt_chechoffs

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/orgt_chechoffs'
db = SQLAlchemy(application)

# @application.route('/')
def hello_world():
    print(db)
    db.create_all()
    return 'Hello World'

# @application.route('/idk')
# def print_db():
#     return db

class Checkoff_sheet(db.Model):
        __tablename__ = 'checkoff_sheet'
        chk_name = Column('chk_name', String(45), primary_key = True)
        sname = Column('sname', String(45))

@application.route('/')
def idk():
        return render_template('login.html') # searches for the templates folder for the .html file
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


@application.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      print(user)
      return redirect(url_for('success',name = user, dumb_var= "dummy :)"))
   else: # request.method == 'GET'
      user = request.args.get('nm')
      return redirect(url_for('success',name = user, dumb_var= "dummy :)"))

# @app.route('/<string:page_name>/')
# def render_static(page_name):
#         return render_template('%s.html' % page_name)</string:page_name>

@application.route('/success/<name><dumb_var>')
def success(name, dumb_var):
   return 'welcome %s, %s' % (name, dumb_var)

if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)      

#todo: shouldn't a checkoff belong to a sport or a checkoff sheet?