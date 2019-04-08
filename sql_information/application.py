from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
        chk_name = db.Column('chk_name', db.VARCHAR(45), primary_key = True)
        sname = db.Column('sname', db.VARCHAR(45))

@application.route('/')
def idk():
    result = db.engine.execute('SELECT * FROM checkoff_sheet')
    names = [row[0] for row in result]
    return names[0]

if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)