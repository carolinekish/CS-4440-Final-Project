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
    """
    Create checkoff sheet for staff member
    :param name:    name of staff member sheet is for
    """
    import json
    f = open("docs/mongodb_design/rcsheet.txt", "r")
    doc = json.load(f)
    f.close()
    doc["_id"] = generate_id(name)
    insert_document_checkoff_sheets_collection(doc)

def find_checkoff_location(name, checkoff_name):
    """
    Find appropriate indeces in checkoff_sheet document that correspond to the desired checkoff to be given
    :param name: name of staff member checkoff is for
    :param checkoff_name: name of checkoff requirement to be given 
    """
    id = generate_id(name)
    doc = select_document_checkoff_sheets_collection(id)
    i, j, k = (0, 0, 0)
    for i in range(len(doc["categories"])):
        for j in range(len(doc["categories"][i]["checkoffs"])):
            for k in range(len(doc["categories"][i]["checkoffs"][j]["requirements"])):
                if doc["categories"][i]["checkoffs"][j]["requirements"][k]["description"] == checkoff_name:
                    return i, j, k
    return i, j, k

def give_checkoff(name, checkoff_name, auth_by):
    """
    Give checkoff to staff memeber
    :param name:              name of staff member checkoff is for
    :param checkoff_name:     name of checkoff requirement (associated w checkbox)
    :param auth_by:           current user authorizing the checkoff
    """
    i, j, k = find_checkoff_location(name, checkoff_name)
    update_document_checkoff_sheets_collection(generate_id(name), cat_index=i, check_index=j, req_index=k, authorized_by=auth_by)

if __name__=="__main__":
    pass
    # i, j, k = find_checkoff_location("caroline", "test_two")
    # update_document_checkoff_sheets_collection(generate_id("caroline"), cat_index=i, check_index=j, req_index=k, authorized_by="me!")
    # create_checkoff_sheet_for_staff("caroline")
