import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  String, Column
from flask_table import Table, Col
application = Flask(__name__)
# USE orgt_chechoffs

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://orgt4440:finalproject4440@orgt4440.ccfdnjnpnqku.us-east-2.rds.amazonaws.com:3306/orgt_chechoffs'
db = SQLAlchemy(application)

class ItemTable(Table):
    name = Col('Name')
    abbreviation = Col('Abbreviation')

class Position(db.Model):
        __tablename__ = 'position'
        name = Column('name', String(45), primary_key=True)
        abbreviation = Column('abbreviation', String(5))

# # Get some objects
# class Item(object):
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description

# result = db.engine.execute('SELECT * FROM position')

# items = result.fetchall()


start = time.time()
items = Position.query.all()
end = time.time()
duration = end - start
print(duration)

table = ItemTable(items)

@application.route('/')
def hello_world():
    return table.__html__() + "<br>" + str(duration)

# Print the html
# print(table.__html__())
# or just {{ table }} from within a Jinja template