from db_handler import *
from logic import *

def main():
    # set up staff_members collection
    f = open("docs/mongodb_design/rcstaff.txt", "r")
    staff_list = json.load(f)
    f.close()
    insert_document_staff_members_collection(staff_list)

    # set up checkoff_sheets collection
    names = [doc["name"] for doc in staff_list]
    for name in names:
        create_checkoff_sheet_for_staff(name)
    # create rock climbing sport checkoff sheet
    create_checkoff_sheet_for_staff("rock climbing")

    # set up sports collection 
    f = open("docs/mongodb_design/sports.txt", "r")
    sports_list = json.load(f)
    f.close()
    insert_document_sports_collection(sports_list)

if __name__=="__main__":
    main()
