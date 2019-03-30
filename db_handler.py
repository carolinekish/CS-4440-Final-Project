import pymongo
from pymongo import MongoClient

connection = None

def connect():
    """connect to mongodb's orgt database and initialize global 'connection' variable"""
    global connection
    connection = MongoClient()
    return connection.orgt_db

def disconnect():
    """disconnet from mongodb's orgt database"""
    global connection
    connection.close()
