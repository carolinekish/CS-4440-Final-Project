import pymongo
import json
from pymongo import MongoClient
import ssl

connection = None
db = None

def connect():
    """
    connect to mongodb's orgt database and initialize global 'connection' variable
    """
    global connection
    global db

    # MongoDB Local
    # connection = MongoClient()
    # db = connection.orgt_db

    # MongoDB Atlas
    connection = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-bt4cv.mongodb.net/test?retryWrites=true", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    db = connection.atlas_orgt


def disconnect():
    """
    disconnet from mongodb's orgt database
    """
    global connection
    connection.close()

# checkoff_sheets collection functions

def insert_document_checkoff_sheets_collection(doc):
    """
    insert document (or many documents) into checkoff_sheets collection
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
    """select checkoff sheet of staff member whose name corresponds to id"""
    try:
        connect()
        if id is None:
            # result is an 'iterator' of dict obj
            # each dict obj is a document and can be treated
            # like a regular python dict
            result = db.checkoff_sheets.find()
        else:
            # return first (ONLY) doc associated with id as dict
            result = db.checkoff_sheets.find({"_id": id})[0]
        disconnect()
        return result
    except Exception as ex:
        print("select_document_checkoff_sheets_collection error: {}".format(ex))

def delete_document_checkoff_sheets_collection(id=None):
    """delete checkoff sheet corresponding to id"""
    try:
        connect()
        result = db.checkoff_sheets.delete_one({"_id": id})
        # result.deleted_count -> # of deleted documents
        # result.acknowledged -> True if operation with write concern and false if write concern was disabeled
        disconnect()
        return result
    except Exception as ex:
        print("delete_document_checkoff_sheets_collection error: {}".format(ex))

def update_document_checkoff_sheets_collection(id, cat_index, check_index, req_index, authorized_by):
    """give checkoff to person corresponding to id"""
    try:
        connect()
        import datetime
        update_string_date =  "categories.{}.checkoffs.{}.requirements.{}.date_fulfilled".format(cat_index, check_index, req_index)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        update_string_auth = "categories.{}.checkoffs.{}.requirements.{}.authorized_by".format(cat_index, check_index, req_index)
        db.checkoff_sheets.update_one({"_id": id}, {"$set": {update_string_date: date, update_string_auth: authorized_by}})
        disconnect()
    except Exception as ex:
        print("update_document_checkoff_sheets_collection error: {}".format(ex))

def update_document_checkoff_sheet_colleciton_change_checkoff(id, cat_index, check_index, new_req_description):
    """add checkoff requirement to sport with id's checkoff sheet"""
    try:
        connect()
        update_string = "categories.{}.checkoffs.{}.requirements".format(cat_index, check_index)
        db.checkoff_sheets.update_one({"_id": id},{"$push": {update_string: {"description": new_req_description, "date_fulfilled": "N/A", "authorized_by": "N/A"}}})
        disconnect()
    except Exception as ex:
        print("update_document_checkoff_sheet_colleciton_change_checkoff error: {}".format(ex))


# staff members collection functions

def insert_document_staff_members_collection(doc):
    """
    insert document (or many documents) into staff_members collection
    """
    try:
        connect()
        if type(doc) == list:
            db.staff_members.insert_many(doc)
        else:
            db.staff_members.insert_one(doc)
        disconnect()
    except Exception as ex:
        print("insert_document_staff_members_collection error: {}".format(ex))

def select_document_staff_members_collection(name=None):
    """
    select staff_member info whose name corresponds to name
    """
    try:
        connect()
        if name is None:
            result = db.staff_members.find()
        else:
            result = db.staff_members.find({"name": name})[0]
        disconnect()
        return result
    except Exception as ex:
        print("select_document_staff_members_collection error: {}".format(ex))

# sports collection functions

def insert_document_sports_collection(doc):
    """
    insert document (or many documents) into sports collection
    """
    try:
        connect()
        if type(doc) == list:
            db.sports.insert_many(doc)
        else:
            db.sports.insert_one(doc)
        disconnect()
    except Exception as ex:
        print("insert_document_sports_collection error: {}".format(ex))
        
# debugging
if __name__=="__main__":
    pass
