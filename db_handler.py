import pymongo
import json
from pymongo import MongoClient

connection = None
db = None

def connect():
    """
    connect to mongodb's orgt database and initialize global 'connection' variable
    """
    global connection
    global db
    connection = MongoClient()
    db = connection.orgt_db

def disconnect():
    """
    disconnet from mongodb's orgt database
    """
    global connection
    connection.close()

def insert_document_checkoff_sheets_collection(doc):
    """
    insert document into checkoff_sheets collection
    """
    try:
        connect()
        if type(doc) == list:
            db.checkoff_sheets.insert_many(doc)
        else:
            db.checkoff_sheets.insert_one(doc)
        disconnect()
    except Exception as ex:
        print("insert_document_checkoff_sheets_collection_ error: {}".format(ex))

def select_document_checkoff_sheets_collection(id=None):
    try:
        connect()
        if id is None:
            # result is an 'iterator' of dict obj
            # each dict obj is a document and can be treated
            # like a regular python dict
            result = db.checkoff_sheets.find()
        else:
            result = db.checkoff_sheets.find({"_id": id})
        disconnect()
        return result
    except Exception as ex:
        print("select_document_checkoff_sheets_collection error: {}".format(ex))

def delete_document_checkoff_sheets_collection(id=None):
    try:
        connect()
        result = db.checkoff_sheets.delete_one({"_id": id})
        # result.deleted_count -> # of deleted documents
        # result.acknowledged -> True if operation with write concern and false if write concern was disabeled
        disconnect()
        return result
    except Exception as ex:
        print("delete_document_checkoff_sheets_collection error: {}".format(ex))

def insert_document_staff_members_collection():
    pass 

# debugging
if __name__=="__main__":
    print()
    # insert_document_checkoff_sheets_collection({"_id": 4})
    delete_document_checkoff_sheets_collection(2)
    result = select_document_checkoff_sheets_collection()
    for doc in result:
        print(doc["_id"])
    print()