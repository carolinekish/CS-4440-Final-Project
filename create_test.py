from db_handler import *
from logic import *

if __name__=="__main__":
    delete_document_checkoff_sheets_collection(845)
    insert_document_checkoff_sheets_collection({"_id": 845, "categories": [{"cat_name": "test_one_cat", "checkoffs": [{"requirements": [{"description": "test_one_1", "date_fulfilled": "N/A"}, {"description": "test_one_2", "date_fulfilled": "N/A"}]}]}, {"cat_name": "test_two_cat", "checkoffs": [{"requirements": [{"description": "test_two", "date_fulfilled": "N/A"}]}]}]})
    print("ready for testing...")
