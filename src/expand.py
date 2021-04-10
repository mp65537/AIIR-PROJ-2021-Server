from copy import deepcopy

#deepcopy check

def expand_config_tree(build_config):
    build_data = deepcopy(build_config)
    build_vars = build_data["vars"]
    del build_data["vars"]
    validate_vars(build_vars)
    vaildate_dict(build_data)
    return expand_vars_in_dict(build_data, build_vars)

def expand_vars_in_dict(input_dict, build_vars):
    result_dict = {}
    for item_name, item_value in input_dict.items():
        if isinstance(item_value, str):
            result_value = expand_vars_in_string(
                item_value, build_vars)
        elif isinstance(item_value, list):
            result_value = expand_vars_in_list(
                item_value, build_vars)
        elif isinstance(item_value, dict):
            result_value = expand_vars_in_dict(
                item_value, build_vars)
        else:
            result_value = item_value
        result_dict[expand_vars_in_string(
                item_name, build_vars)] = result_value
    return result_dict

def expand_vars_in_list(input_list, build_vars):
    result_list = []
    for item in input_list:
        if (item[:2] == "$(") and (item[-1:] == ")"):
            var_name = item[2:-1]
            var_value = build_vars.get(var_name, None)
            if var_value is None:
                raise ExpandError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                result_list.extend(var_value)
            else:
                result_list.append(var_value)
            continue
        result_list.append(expand_vars_in_string(item, build_vars))
    return result_list

def expand_vars_in_string(input_string, build_vars):
    expand_offset = 0
    result_string = ""
    while True:
        var_offset = input_string.find("$", expand_offset)
        if var_offset < 0:
            break
        if input_string[var_offset + 1] == '(':
            result_string += input_string[expand_offset:var_offset]
            var_end_offset = input_string.find(")", var_offset + 2)
            if var_end_offset < 0:
                raise ExpandError("Expected ')' after '$(' token")
            var_name = input_string[var_offset + 2:var_end_offset]
            var_value = build_vars.get(var_name, None)
            if var_value is None:
                raise ExpandError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                var_value = " ".join(var_value)
            result_string += var_value
            expand_offset = var_end_offset + 1
        else:
            result_string += input_string[expand_offset:var_offset + 1]
            expand_offset = var_offset + 1
    result_string += input_string[expand_offset:]
    return result_string

def vaildate_dict(input_dict):
    for item_name, item_value in input_dict.items():
        if not isinstance(item_name, str):
            raise BadFormatError("Entry names have to be strings")
        if isinstance(item_value, list):
            validate_list(item_value)
        elif isinstance(item_value, dict):
            vaildate_dict(item_value)
        elif not (isinstance(item_value, str) or isinstance(item_value, bool)):
            raise BadFormatError("Variables have to be strings or lists")

def validate_vars(build_vars):
    for var_name, var_value in build_vars.items():
        if not isinstance(var_name, str):
            raise BadFormatError("Variable names have to be strings")
        if isinstance(var_value, list):
            validate_list(var_value)
        elif not isinstance(var_value, str):
            raise BadFormatError("Variables have to be strings or lists")

def validate_list(input_list):
    for item in input_list:
        if not isinstance(item, str):
            raise BadFormatError("Lists could only have string items")

class BadFormatError(Exception): #rename?
    pass

class ExpandError(Exception):
    pass
