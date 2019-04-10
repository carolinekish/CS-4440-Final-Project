from db_handler import *

def generate_id(name=None):
    """
    Generate unique ObjectID for MongoDB document
    :param name:        name of staff member
    :return:            sum of the ascii values in staff member's name
    """
    if name is None:
        import random
        return random.randint(1, 10000)
    else:
        return sum([ord(l) for l in name])

def create_checkoff_sheet_for_staff(name=""):
    import json
    f = open("docs/mongodb_design/rcsheet.txt", "r")
    doc = json.load(f)
    f.close()
    doc["_id"] = generate_id(name)
    # doc = json.dumps(doc)
    insert_document_checkoff_sheets_collection(doc)

if __name__=="__main__":
    create_checkoff_sheet_for_staff("caroline")
