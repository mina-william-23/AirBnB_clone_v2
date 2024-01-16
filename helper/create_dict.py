"""
Create a dictionary from a list of
arguments and a dictionary of keyword arguments.
"""


def type_checker(value):
    """
    Check the type of a value.
    :param value: value to check
    :return: type of the value
    """
    if(value[0] == '"' and value[-1] == '"'):
        value = value[1:-1].replace('"', '\"').replace('_', ' ')
        return value
    if "." in value:
        try:
            return float(value)
        except ValueError:
            pass
    try:
        return int(value)
    except ValueError:
        pass
    return None


def create_kwargs(list_args, splitter):
    """
    Create a dictionary from a list of arguments
    and a dictionary of keyword arguments.
    :param list_args: list of arguments
    :param kwargs: dictionary of keyword arguments
    :return: dictionary of arguments and keyword arguments
    """
    dict_args = {}
    for arg in list_args:
        if splitter not in arg:
            continue
        key, value = arg.split(splitter)
        value = type_checker(value)
        if value is not None:
            dict_args[key] = value

    return dict_args
