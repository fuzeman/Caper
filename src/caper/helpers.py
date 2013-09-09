def is_list_type(obj, element_type):
    if not type(obj) is list:
        return False

    if len(obj) < 1:
        raise ValueError("Unable to determine list element type from empty list")

    return type(obj[0]) is element_type
