import pymongo
import json
from pymongo import MongoClient

connection = None
db = None

def connect():
    """connect to mongodb's orgt database and initialize global 'connection' variable"""
    global connection
    global db
    connection = MongoClient()
    db = connection.orgt_db

def disconnect():
    """disconnet from mongodb's orgt database"""
    global connection
    connection.close()

def insert_document_checkoff_sheets_collection_(doc):
    try:
        connect()
        db.checkoff_sheets.insert(doc)
        disconnect()
    except Exception as ex:
        print("insert_document_checkoff_sheets_collection_ error: {}".format(ex.getMessage()))

def select_document_checkoff_sheets_collection(id=None):
    try:
        connect()
        if id is None:
            result = db.checkoff_sheets.find()
        else:
            result = db.checkoff_sheets.find({"_id": id})
        disconnect()
    except Exception as ex:
        print("select_document_checkoff_sheets_collection error: {}".format(ex.getMessage()))

# debugging 
if __name__=="__main__":
    pass
