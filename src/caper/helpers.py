def is_list_type(obj, element_type):
    if not type(obj) is list:
        return False

    if len(obj) < 1:
        raise ValueError("Unable to determine list element type from empty list")

    return type(obj[0]) is element_type


def clean_dict(target, remove=None):
    """Recursively remove items matching a value 'remove' from the dictionary

    :type target: dict
    """
    if type(target) is not dict:
        raise ValueError("Target is required to be a dict")

    for key in target.keys():
        if type(target[key]) is not dict:
            if target[key] == remove:
                target.pop(key)
        else:
            clean_dict_items(target[key], remove)

    return target
