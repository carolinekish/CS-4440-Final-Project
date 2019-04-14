import pymongo
import json
from pymongo import MongoClient
from logic import *
from db_handler import *
import time
def main():
    use_explain_func = False
    # connect to database
    connection = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-bt4cv.mongodb.net/test?retryWrites=true", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    db = connection.atlas_orgt

    rcstaff = ["Caroline Kish", "Archie Andrews", "Jughead Jones", "Betty Cooper", "Veronica Lodge", "Cheryl Blossom"]
    if use_explain_func:
        f = open("analytics2.txt", "w")

    # test query time
    for p in rcstaff:
        # f.write("querying checkoff sheet for {}...\n".format(p))
        id = generate_id(p)
        start = time.time()
        give_checkoff("Caroline Kish", "TL must submit a written endorsement to the ADOR. e-mail is fine.", "ADMIN")
        # create_checkoff_sheet_for_staff(p)
        # if use_explain_func:
        #     result = db.checkoff_sheets.find({"_id": id}).explain()
        # else:
        #     result =  db.checkoff_sheet.delete_one({"_id": id})
        end = time.time()
        # f.write(str(result))
        # f.write("\n\n")
        if not use_explain_func:
            print(end - start)
        # print(result)

    # close analytics file
    # f.close()
    # disconnect from database
    connection.close()

if __name__=="__main__":
    main()
