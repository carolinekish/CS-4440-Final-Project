import pymongo
import json
from pymongo import MongoClient
from logic import *
from db_handler import *

def main():
    # connect to database
    connection = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-bt4cv.mongodb.net/test?retryWrites=true", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    db = connection.atlas_orgt

    rcstaff = ["Caroline Kish", "Archie Andrews", "Jughead Jones", "Betty Cooper", "Veronica Lodge", "Cheryl Blossom"]
    f = open("analytics.txt", "w")

    # test query time
    for p in rcstaff:
        f.write("querying checkoff sheet for {}...\n".format(p))
        id = generate_id(p)
        result = db.checkoff_sheets.find({"_id": id}).explain()
        f.write(str(result))
        f.write("\n\n")
        # print(result)

    # close analytics file
    f.close()
    # disconnect from database
    connection.close()

if __name__=="__main__":
    main()
