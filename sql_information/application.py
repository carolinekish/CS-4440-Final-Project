from flask import Flask
from flask_sqlalchemy import SQLAlchemy
application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/idk_what_this_should_be'
db = SQLAlchemy(application)

@application.route('/')
def hello_world():
    print(db)
    return 'Hello World'

# @application.route('/idk')
# def print_db():
#     return db

if __name__ == '__main__':
    application.run()