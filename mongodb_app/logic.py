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

def find_new_req_location(cat_name, checkoff_name, sport="rock climbing"):
    id = generate_id(sport)
    doc = select_document_checkoff_sheets_collection(id)
    i, j = (0, 0)
    for i in range(len(doc["categories"])):
        if doc["categories"][i]["cat_name"] == cat_name:
            for j in range(len(doc["categories"][i]["checkoffs"])):
                if doc["categories"][i]["checkoffs"][j]["check_name"] == checkoff_name:
                    return i, j
    return i, j

# staff member looks up his / her completed checkoffs (USE CASE 1)
def lookup_sheet(name):
    """
    Lookup checkoff sheet of given staff member
    :param name:    name of staff member's checkoff sheet to look up
    :return:        checkoff sheet dictionary associated with name
    """
    return select_document_checkoff_sheets_collection(generate_id(name))

# staff member gives checkoff (USE CASE 2)
def give_checkoff(name, checkoff_name, auth_by):
    """
    Give checkoff to staff memeber
    :param name:              name of staff member checkoff is for
    :param checkoff_name:     name of checkoff requirement (associated w checkbox)
    :param auth_by:           current user authorizing the checkoff
    """
    i, j, k = find_checkoff_location(name, checkoff_name)
    update_document_checkoff_sheets_collection(generate_id(name), cat_index=i, check_index=j, req_index=k, authorized_by=auth_by)

# trip leaders add /remove checkoff from their sport's checkoff sheet (USE CASE 3)
def add_requirement(cat_name, check_name, new_req_description, sport="rock climbing"):
    """
    Add checkoff to sport checkoff sheet
    :param cat_name: category that checkoff requirement will be a part of
    :param check_name: checkoff that requirement will be a part of
    :param new_req_description: description of the added requirement
    """
    i, j = find_new_req_location(cat_name, check_name, sport)
    update_document_checkoff_sheet_colleciton_change_checkoff(generate_id(sport), i, j, new_req_description)

if __name__=="__main__":
    # print(generate_id("rock climbing"))

    pass
    # i, j, k = find_checkoff_location("caroline", "test_two")
    # update_document_checkoff_sheets_collection(generate_id("caroline"), cat_index=i, check_index=j, req_index=k, authorized_by="me!")
    # create_checkoff_sheet_for_staff("caroline")
    # add_requirement(cat_name="test_two_cat", check_name="Dos", new_req_description="HELLO WORLD")
