
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
